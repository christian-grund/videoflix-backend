from django.contrib.auth import get_user_model
from django.test import TestCase
from auth.tokens import AccountActivationTokenGenerator  
import six

User = get_user_model()

class AccountActivationTokenGeneratorTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='password123'
        )
        self.token_generator = AccountActivationTokenGenerator()


    def test_token_generation(self):
        token = self.token_generator.make_token(self.user)

        self.assertTrue(self.token_generator.check_token(self.user, token))


    def test_token_invalid_for_different_user(self):
        # Erstelle einen zweiten Benutzer
        another_user = User.objects.create_user(
            username='anotheruser',
            email='anotheruser@example.com',
            password='password123'
        )

        token = self.token_generator.make_token(self.user)

        # Überprüfe, dass das Token nicht für einen anderen Benutzer gültig ist
        self.assertFalse(self.token_generator.check_token(another_user, token))


