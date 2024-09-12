
from rest_framework import viewsets, status
from rest_framework.response import Response
from django.contrib.auth import authenticate, logout
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


from auth.register.serializers import UserSerializer

class RegisterViewSet(viewsets.ViewSet):
    def create(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User registered successfully!"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
# 07175f9aed0c9cd5e870cbb2ed0adc4dc774e8cf
class LoginViewSet(viewsets.ViewSet):
    def create(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        try:
            # Benutzer anhand der E-Mail finden
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"error": "User with this email does not exist"}, status=status.HTTP_400_BAD_REQUEST)

        # Benutzer authentifizieren
        user = authenticate(username=user.username, password=password)

        if user is not None:
            # Token generieren oder abrufen
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                "message": "Login successful",
                "token": token.key  # Token zurückgeben
            }, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)
        

class LogoutViewSet(viewsets.ViewSet):
    def create(self, request):
        logout(request)
        return Response({"message":"Logout successful"}, status=status.HTTP_200_OK)
