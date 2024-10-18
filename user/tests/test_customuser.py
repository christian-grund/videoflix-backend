from django.test import TestCase
from django.contrib.auth import get_user_model

class CustomUserTests(TestCase):
    
    def setUp(self):
        self.user_data = {
            'username': 'testuser',
            'password': 'testpassword',
            'custom': 'Custom data',
            'phone': '1234567890',
            'address': '123 Test Street'
        }
        self.user = get_user_model().objects.create_user(**self.user_data)

    def test_create_custom_user(self):
        self.assertEqual(self.user.username, self.user_data['username'])
        self.assertTrue(self.user.check_password(self.user_data['password']))
        self.assertEqual(self.user.custom, self.user_data['custom'])
        self.assertEqual(self.user.phone, self.user_data['phone'])
        self.assertEqual(self.user.address, self.user_data['address'])

    def test_custom_user_str(self):
        self.assertEqual(str(self.user), self.user.username)  
