from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from user.models import CustomUser

class UserCheckViewSetTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = CustomUser.objects.create_user(email="testuser@example.com", username= "testuser", password="password123")

    def test_user_exists(self):
        response = self.client.get(reverse('check-email') + '?email=testuser@example.com')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['exists'])

    def test_user_does_not_exist(self):
        response = self.client.get(reverse('check-email') + '?email=nonexistent@example.com')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
