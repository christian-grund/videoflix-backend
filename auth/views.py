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
from .tokens import account_activation_token
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from rest_framework.decorators import api_view


CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)


class SignUpViewSet(viewsets.ViewSet):
    def create(self, request):
        serializer = UserSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            user.is_active = False  # Setze den Benutzer als inaktiv
            user.save()
            
           # Token generieren
            token, created = Token.objects.get_or_create(user=user)
            
            verification_link = f'http://localhost:4200/activate?key={token.key}'
            # current_site = get_current_site(request)
            subject = 'Activate your VIDEOFLIX account'
            message = f'Hi {user.username},\n\nPlease use the link below to activate your account:\n\n'
            message += f'{verification_link}\n\n'
            message += 'Thank you!'
            send_mail(
                subject,
                message,
                settings.EMAIL_HOST_USER,
                ['christian.grund@outlook.de'], # [user.email],
                fail_silently=False,
            )

            return Response({"message": "User registered successfully! Please check your email to activate your account"}, status=status.HTTP_201_CREATED)
        
        print("Serializer errors:", serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def ActivateAccountView(request):
    token = request.data.get('token')
    
    try:
        user = Token.objects.get(key=token).user
        user.is_active = True
        user.save()
        
        return Response({"message": "Account activated successfully!"}, status=status.HTTP_200_OK)
    except Token.DoesNotExist:
        return Response({"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)
    

class LoginViewSet(viewsets.ViewSet):
    def create(self, request):
        token_key = request.query_params.get('key')
        
        if token_key:
            try:
                token = Token.objects.get(key=token_key)
                user = token.user
                # Optional: Token als "verbraucht" markieren
                # token.delete()
                
                # Benutzer authentifizieren (Optional, falls du es benötigst)
                user = authenticate(username=user.username, password=request.data.get('password'))
                
                if user is not None:
                    return Response({
                        "message": "Login successful",
                        "token": token.key
                    }, status=status.HTTP_200_OK)
                else:
                    return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)
                
            except Token.DoesNotExist:
                return Response({"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({"error": "No token provided"}, status=status.HTTP_400_BAD_REQUEST)


    
# 07175f9aed0c9cd5e870cbb2ed0adc4dc774e8cf
# TTL = Total Life Time, Variable aus Settings, kann man auch direkt reinschreiben (z.B. 15 * 60s), Angabe in Sekunden
# @cache_page(CACHE_TTL) 
# class LoginViewSet(viewsets.ViewSet):

#     @method_decorator(cache_page(CACHE_TTL))
#     def create(self, request):
#         email = request.data.get('email')
#         password = request.data.get('password')

#         try:
#             # Benutzer anhand der E-Mail finden
#             user = User.objects.get(email=email)
#         except User.DoesNotExist:
#             return Response({"error": "User with this email does not exist"}, status=status.HTTP_400_BAD_REQUEST)

#         # Benutzer authentifizieren
#         user = authenticate(username=user.username, password=password)

#         if user is not None:
#             # Token generieren oder abrufen
#             token, created = Token.objects.get_or_create(user=user)
#             return Response({
#                 "message": "Login successful",
#                 "token": token.key  # Token zurückgeben
#             }, status=status.HTTP_200_OK)
#         else:
#             return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)
        

class LogoutViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def create(self, request):
        # Token des Benutzers löschen
        try:
            request.user.auth_token.delete()
            return Response({"message": "Logout successful!"}, status=status.HTTP_200_OK)
        except Token.DoesNotExist:
            return Response({"error": "User is not logged in."}, status=status.HTTP_400_BAD_REQUEST)
