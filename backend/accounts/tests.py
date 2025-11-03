from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status

class AccountTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_user_registration(self):
        url = '/api/accounts/register/'
        data = {'username': 'testuser', 'email': 'test@example.com', 'password': 'testpassword'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, 'testuser')
