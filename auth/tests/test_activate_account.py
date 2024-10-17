from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from rest_framework.authtoken.models import Token
from user.models import CustomUser

class ActivateAccountViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = CustomUser.objects.create_user(email="testuser@example.com", username= "testuser", password="password123", is_active=False)
        self.token = Token.objects.create(user=self.user)

    def test_activate_account_success(self):
        data = {"token": self.token.key}
        response = self.client.post(reverse('activate-account'), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertTrue(self.user.is_active)

    def test_activate_account_invalid_token(self):
        data = {"token": "invalidtoken"}
        response = self.client.post(reverse('activate-account'), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
