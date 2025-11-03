from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from feed.models import Post
from .models import Cart

class MarketplaceTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.force_authenticate(user=self.user)
        self.product = Post.objects.create(author=self.user, content='Test Product', is_product=True, price=10.00)
        self.cart = Cart.objects.get(user=self.user)

    def test_add_item_to_cart(self):
        url = f'/api/marketplace/cart/{self.cart.id}/add_item/'
        data = {'product_id': self.product.id, 'quantity': 2}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.cart.items.count(), 1)
        self.assertEqual(self.cart.items.first().quantity, 2)

    def test_checkout(self):
        self.cart.items.create(product=self.product, quantity=1)
        url = '/api/marketplace/checkout/'
        response = self.client.post(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(self.cart.items.count(), 0)
