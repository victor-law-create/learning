from rest_framework import viewsets, permissions, status, mixins, views
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Cart, CartItem, Order, OrderItem
from .serializers import CartSerializer, CartItemSerializer
from feed.models import Post
from decimal import Decimal

class CartViewSet(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    @action(detail=True, methods=['post'])
    def add_item(self, request, pk=None):
        cart = self.get_object()
        product_id = request.data.get('product_id')
        quantity = request.data.get('quantity', 1)

        if not product_id:
            return Response({'error': 'Product ID is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            product = Post.objects.get(id=product_id, is_product=True)
        except Post.DoesNotExist:
            return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        if not created:
            cart_item.quantity += int(quantity)
        else:
            cart_item.quantity = int(quantity)
        cart_item.save()

        serializer = CartSerializer(cart)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def remove_item(self, request, pk=None):
        cart = self.get_object()
        item_id = request.data.get('item_id')

        if not item_id:
            return Response({'error': 'Item ID is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            item = CartItem.objects.get(id=item_id, cart=cart)
            item.delete()
        except CartItem.DoesNotExist:
            return Response({'error': 'Item not found in cart'}, status=status.HTTP_404_NOT_FOUND)

        serializer = CartSerializer(cart)
        return Response(serializer.data)

class CheckoutView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        cart = Cart.objects.get(user=request.user)
        if not cart.items.exists():
            return Response({'error': 'Your cart is empty'}, status=status.HTTP_400_BAD_REQUEST)

        total_price = sum(item.product.price * item.quantity for item in cart.items.all())
        total_price_with_fee = total_price * Decimal('1.12')

        order = Order.objects.create(user=request.user, total_price=total_price_with_fee)
        for item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price
            )
        cart.items.all().delete()

        return Response({'success': 'Order created successfully', 'order_id': order.id}, status=status.HTTP_201_CREATED)
