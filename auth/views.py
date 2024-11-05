from django.conf import settings
from django.core.mail import send_mail
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.contrib.auth import authenticate
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authtoken.models import Token
from auth.serializers import UserSerializer
from rest_framework.decorators import api_view, permission_classes, method_decorator
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator
from django.utils.html import strip_tags
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.http import JsonResponse
from user.models import CustomUser

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)


class SignUpViewSet(viewsets.ViewSet):
    """
    Handles user registration, validates input, and sends an activation email.
    """
    permission_classes = [AllowAny]

    def create(self, request):
        serializer = UserSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            user.is_active = False  
            user.save()
            token, created = Token.objects.get_or_create(user=user)
            send_activation_email(user, token)

            return JsonResponse({"message": "User registered successfully! Please check your email to activate your account"}, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

def send_activation_email(user, token):
    """
    Sends an account activation email to the user with a verification link.
    """
    verification_link = f'https://videoflix.christian-grund.dev/activate?key={token.key}'
    subject = 'Activate your VIDEOFLIX account'
    
    html_content = render_to_string('activation_email.html', {
        'username': user.username,
        'verification_link': verification_link,
    })
    
    email = EmailMultiAlternatives(
        subject,
        '',  
        settings.EMAIL_HOST_USER,
        [user.email], 
    )
    
    email.attach_alternative(html_content, "text/html")
    email.send(fail_silently=False)


@api_view(['POST'])
@permission_classes([AllowAny])
def ActivateAccountView(request):
    """
    Activates the user account associated with the provided token.
    """
    token = request.data.get('token')
    
    try:
        user = Token.objects.get(key=token).user
        user.is_active = True
        user.save()
        
        return Response({"message": "Account activated successfully!"}, status=status.HTTP_200_OK)
    except Token.DoesNotExist:
        return Response({"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)


@cache_page(CACHE_TTL) 
class LoginViewSet(viewsets.ViewSet):
    """
    Handles user login and generates a token for authenticated users.
    """
    permission_classes = [AllowAny]
    
    @method_decorator(cache_page(CACHE_TTL))
    def create(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        
        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            return Response({"error": "User with this email does not exist"}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(username=user.username, password=password)

        if user is not None:
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                "message": "Login successful",
                "token": token.key  
            }, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)
        

class LogoutViewSet(viewsets.ViewSet):
    """
    Logs out the authenticated user by deleting their auth token.
    """
    permission_classes = [IsAuthenticated] 

    def create(self, request):
        if request.user.is_authenticated:
            try:
                request.user.auth_token.delete()
                return Response({"message": "Logout successful!"}, status=status.HTTP_200_OK)
            except Token.DoesNotExist:
                return Response({"error": "User is not logged in."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": "User is not authenticated."}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
@permission_classes([AllowAny])
def PasswordResetRequest(request):
    """
    Sends a password reset link to the user's email if it exists.
    """
    email = request.data.get('email')
    try:
        user = CustomUser.objects.get(email=email)
    except CustomUser.DoesNotExist:
        return Response({"error": "User with this email does not exist"}, status=status.HTTP_400_BAD_REQUEST)

    token = default_token_generator.make_token(user)
    reset_link = f'https://videoflix.christian-grund.dev/reset-password?token={token}&uid={user.pk}'
    
    subject = 'VIDEOFLIX Password Reset Request'
    html_content = render_to_string('password_reset_email.html', {
        'username': user.username,
        'reset_link': reset_link,
    })
    
    text_content = strip_tags(html_content)  
    
    send_mail(
        subject,
        text_content,
        settings.EMAIL_HOST_USER,
        [user.email], 
        fail_silently=False,
        html_message=html_content
    )
    
    return Response({"message": "Password reset link sent successfully"}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def PasswordResetConfirm(request):
    """
    Resets the user's password if the provided token is valid.
    """
    token = request.data.get('token')
    uid = request.data.get('uid')
    new_password = request.data.get('new_password')

    try:
        user = CustomUser.objects.get(pk=uid)
    except CustomUser.DoesNotExist:
        return Response({"error": "Invalid user"}, status=status.HTTP_400_BAD_REQUEST)
    
    if default_token_generator.check_token(user, token):
        user.set_password(new_password)
        user.save()
        return Response({"message": "Password reset successful"}, status=status.HTTP_200_OK)
    else:
        return Response({"error": "Invalid or expired token"}, status=status.HTTP_400_BAD_REQUEST)
    

class UserCheckViewSet(viewsets.ViewSet):
    """
    Checks if a user with the specified email address exists.
    """
    permission_classes = [AllowAny]

    def list(self, request):
        email = request.query_params.get('email')
        if email:
            try:
                user = CustomUser.objects.get(email=email)
                return Response({"exists": True}, status=status.HTTP_200_OK)
            except CustomUser.DoesNotExist:
                return Response({"exists": False}, status=status.HTTP_404_NOT_FOUND)
        return Response({"error": "Email parameter is required"}, status=status.HTTP_400_BAD_REQUEST)