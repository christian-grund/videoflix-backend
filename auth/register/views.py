
from rest_framework import viewsets, status
from rest_framework.response import Response
from django.contrib.auth import authenticate, logout

from auth.register.serializers import UserSerializer

class RegisterViewSet(viewsets.ViewSet):
    def create(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User registered successfully!"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
class LoginViewSet(viewsets.ViewSet):
    def create(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)

        if user:
            return Response({"message":"Login successful"}, status=status.HTTP_200_OK)
        else:
            return Response({"message":"Invalid credentials111"}, status=status.HTTP_400_BAD_REQUEST)
        

class LogoutViewSet(viewsets.ViewSet):
    def create(self, request):
        logout(request)
        return Response({"message":"Logout successful"}, status=status.HTTP_200_OK)
