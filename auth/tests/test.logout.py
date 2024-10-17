from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from rest_framework.authtoken.models import Token
from user.models import CustomUser

class LogoutViewSetTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = CustomUser.objects.create_user(email="testuser@example.com", password="password123")
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_logout_success(self):
        response = self.client.post(reverse('logout'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("Logout successful", response.data['message'])

    def test_logout_no_token(self):
        self.client.credentials()  # Remove credentials
        response = self.client.post(reverse('logout'))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
