from django.conf import settings
from django.core.mail import send_mail
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.contrib.auth import authenticate, logout
from django.contrib.auth.models import User
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from auth.serializers import SimpleSerializer, UserSerializer
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator


CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)


class SignUpViewSet(viewsets.ViewSet):
    def create(self, request):
        serializer = UserSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            print("User created:", user)
            print("User mail:", user.email)
            
            # send_mail(
            #     'Willkommen bei unserer Plattform',
            #     f'Hallo {user.username},\n\nDanke für deine Registrierung!',
            #     settings.DEFAULT_FROM_EMAIL,
            #     [user.email],
            #     fail_silently=False,
            # )
            send_mail(
                'Test-E-Mail',
                'Dies ist eine Test-E-Mail.',
                'grund7@gmail.com',
                ['christian.grund@outlook.de'],
                fail_silently=False,
            )
            return Response({"message": "User registered successfully!"}, status=status.HTTP_201_CREATED)
        
        print("Serializer errors:", serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    
# 07175f9aed0c9cd5e870cbb2ed0adc4dc774e8cf
# TTL = Total Life Time, Variable aus Settings, kann man auch direkt reinschreiben (z.B. 15 * 60s), Angabe in Sekunden
# @cache_page(CACHE_TTL) 
class LoginViewSet(viewsets.ViewSet):

    @method_decorator(cache_page(CACHE_TTL))
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
    permission_classes = [IsAuthenticated]

    def create(self, request):
        # Token des Benutzers löschen
        try:
            request.user.auth_token.delete()
            return Response({"message": "Logout successful!"}, status=status.HTTP_200_OK)
        except Token.DoesNotExist:
            return Response({"error": "User is not logged in."}, status=status.HTTP_400_BAD_REQUEST)
