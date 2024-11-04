from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from user.models import CustomUser

class SignUpViewSetTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_signup_success(self):
        data = {
            "email": "testuser@example.com",
            "username": "testuser",
            "password": "password123"
        }
        response = self.client.post(reverse('SignUpView'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response_json = response.json()
        self.assertIn("User registered successfully", response_json['message'])

    def test_signup_invalid_data(self):
        data = {
            "email": "invalidemail",
            "password": "password123"
        }
        response = self.client.post(reverse('SignUpView'), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
