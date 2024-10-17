from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from user.models import CustomUser

class PasswordResetTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = CustomUser.objects.create_user(email="testuser@example.com", username= "testuser", password="password123")

    def test_password_reset_request_success(self):
        data = {"email": "testuser@example.com"}
        response = self.client.post(reverse('password_reset_request'), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("Password reset link sent successfully", response.data['message'])

    def test_password_reset_invalid_email(self):
        data = {"email": "invalid@example.com"}
        response = self.client.post(reverse('password_reset_request'), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
