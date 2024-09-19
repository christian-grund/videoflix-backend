from rest_framework import serializers
from django.contrib.auth.models import User

from user.models import CustomUser


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    email = serializers.EmailField(required=True)

    class Meta:
        model = CustomUser
        fields = ['email', 'password']

    def validate_email(self, value):
        if CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value

    def create(self, validated_data):
        email = validated_data['email']
        username = email.split('@')[0]
        
        user = CustomUser.objects.create_user(
            username=username,
            email=email,
            password=validated_data['password']
        )
        
        return user
