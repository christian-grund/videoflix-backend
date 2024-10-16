from rest_framework import serializers
from django.contrib.auth.models import User

from user.models import CustomUser


class UserSerializer(serializers.ModelSerializer):
    """
    Handles user registration and validation for the CustomUser model.
    - Validates the uniqueness of the email address.
    - Extracts the username from the email address.
    - Creates a new user instance with the provided email and password.
    """
    password = serializers.CharField(write_only=True)
    email = serializers.EmailField(required=True)

    class Meta:
        model = CustomUser
        fields = ['email', 'password']

    def validate_email(self, value: str) -> str:
        if self.email_exists(value):
            raise serializers.ValidationError("A user with this email already exists.")
        return value

    def email_exists(self, email: str) -> bool:
        return CustomUser.objects.filter(email=email).exists()

    def create(self, validated_data: dict) -> CustomUser:
        return self.create_user(validated_data)

    def create_user(self, validated_data: dict) -> CustomUser:
        email = validated_data['email']
        username = self.extract_username(email)
        return CustomUser.objects.create_user(
            username=username,
            email=email,
            password=validated_data['password']
        )

    def extract_username(self, email: str) -> str:
        return email.split('@')[0]
