from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from user.models import CustomUser

class LoginViewSetTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = CustomUser.objects.create_user(email="testuser@example.com", username= "testuser", password="password123")

    def test_login_success(self):
        data = {"email": "testuser@example.com", "password": "password123"}
        response = self.client.post(reverse('LoginView'), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)

    def test_login_invalid_credentials(self):
        data = {"email": "testuser@example.com", "password": "wrongpassword"}
        response = self.client.post(reverse('LoginView'), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
