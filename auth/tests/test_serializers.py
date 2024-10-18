from rest_framework.exceptions import ValidationError
from rest_framework.test import APITestCase
from user.models import CustomUser
from auth.serializers import UserSerializer

class UserSerializerTest(APITestCase):

    def setUp(self):
        self.valid_data = {
            'email': 'testuser@example.com',
            'password': 'password123'
        }

    def test_create_user_with_valid_data(self):
        serializer = UserSerializer(data=self.valid_data)
        self.assertTrue(serializer.is_valid())
        user = serializer.save()
        
        self.assertEqual(user.email, self.valid_data['email'])
        self.assertTrue(user.check_password(self.valid_data['password']))
        self.assertEqual(user.username, 'testuser')

    def test_email_uniqueness_validation(self):
        CustomUser.objects.create_user(
            username='existinguser',
            email=self.valid_data['email'],
            password='password123'
        )
        
        serializer = UserSerializer(data=self.valid_data)
        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)

    def test_extract_username_from_email(self):
        serializer = UserSerializer()
        username = serializer.extract_username('testuser@example.com')
        self.assertEqual(username, 'testuser')

    def test_validate_email_when_email_does_not_exist(self):
        serializer = UserSerializer(data=self.valid_data)
        self.assertTrue(serializer.is_valid())
        
    def test_validate_email_when_email_exists(self):
        CustomUser.objects.create_user(
            username='existinguser',
            email='existinguser@example.com',
            password='password123'
        )
        
        valid_data = {
            'email': 'newuser@example.com',
            'password': 'password123'
        }
        serializer = UserSerializer(data=valid_data)
        self.assertTrue(serializer.is_valid())

        invalid_data = {
            'email': 'existinguser@example.com',
            'password': 'password123'
        }
        serializer = UserSerializer(data=invalid_data)
        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)

