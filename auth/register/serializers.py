from rest_framework import serializers
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = ['email', 'password']

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value

    
    def create(self, validated_data):
        email = validated_data['email']
        username = email.split('@')[0]
        
        return User.objects.create(
            username = username,
            email = email,
            password = validated_data['password']
        )
        

    