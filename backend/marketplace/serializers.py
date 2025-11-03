from rest_framework import serializers
from .models import Cart, CartItem
from feed.serializers import PostSerializer

class CartItemSerializer(serializers.ModelSerializer):
    product = PostSerializer(read_only=True)

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity']

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = ['id', 'user', 'items', 'created_at']
