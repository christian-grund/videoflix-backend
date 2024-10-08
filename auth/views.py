from django.conf import settings
from django.core.mail import send_mail
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.contrib.auth import authenticate
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authtoken.models import Token
from auth.serializers import UserSerializer
from rest_framework.decorators import api_view
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator
from django.utils.html import strip_tags


from user.models import CustomUser
# from django.contrib.auth.models import User


CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)

def send_activation_email(user, token):
    verification_link = f'http://localhost:4200/activate?key={token.key}'
    subject = 'Activate your VIDEOFLIX account'
    
    html_content = render_to_string('activation_email.html', {
        'username': user.username,
        'verification_link': verification_link,
    })
    
    email = EmailMultiAlternatives(
        subject,
        '',  
        settings.EMAIL_HOST_USER,
        ['christian.grund@outlook.de'], # user.email
    )
    
    email.attach_alternative(html_content, "text/html")
    
    email.send(fail_silently=False)


class SignUpViewSet(viewsets.ViewSet):
    def create(self, request):
        serializer = UserSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            user.is_active = False  
            user.save()
            
            token, created = Token.objects.get_or_create(user=user)
            
            send_activation_email(user, token)

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
        print('ActivateAccount user:', user)
        
        return Response({"message": "Account activated successfully!"}, status=status.HTTP_200_OK)
    except Token.DoesNotExist:
        return Response({"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)
    


           

# TTL = Total Life Time, Variable aus Settings, kann man auch direkt reinschreiben (z.B. 15 * 60s), Angabe in Sekunden
# @cache_page(CACHE_TTL) 
class LoginViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny]
    
    # @method_decorator(cache_page(CACHE_TTL))
    def create(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        print(f"Email: {email}, Password: {password}")
        
        try:
            user = CustomUser.objects.get(email=email)
            print(f"User found: {user}")
        except CustomUser.DoesNotExist:
            print(f"No user found with email: {email}")
            return Response({"error": "User with this email does not exist"}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(username=user.username, password=password)
        print(f"Authentication result: {user}")
        print(f"Username: {user.username}")

        if user is not None:
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                "message": "Login successful",
                "token": token.key  # Neuen Token zurückgeben
            }, status=status.HTTP_200_OK)
        else:
            print("Invalid credentials")
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


@api_view(['POST'])
def PasswordResetRequest(request):
    email = request.data.get('email')
    try:
        user = CustomUser.objects.get(email=email)
    except CustomUser.DoesNotExist:
        return Response({"error": "User with this email does not exist"}, status=status.HTTP_400_BAD_REQUEST)

    token = default_token_generator.make_token(user)
    reset_link = f'http://localhost:4200/reset-password?token={token}&uid={user.pk}'
    
    subject = 'VIDEOFLIX Password Reset Request'
    html_content = render_to_string('password_reset_email.html', {
        'username': user.username,
        'reset_link': reset_link,
    })
    
    text_content = strip_tags(html_content)  # Fallback für E-Mail-Clients, die HTML nicht unterstützen
    
    send_mail(
        subject,
        text_content,
        settings.EMAIL_HOST_USER,
        ['christian.grund@outlook.de'],
        fail_silently=False,
        html_message=html_content
    )
    
    return Response({"message": "Password reset link sent successfully"}, status=status.HTTP_200_OK)


@api_view(['POST'])
def PasswordResetConfirm(request):
    token = request.data.get('token')
    uid = request.data.get('uid')
    new_password = request.data.get('new_password')
    print('new_password:', new_password)

    try:
        user = CustomUser.objects.get(pk=uid)
    except CustomUser.DoesNotExist:
        return Response({"error": "Invalid user"}, status=status.HTTP_400_BAD_REQUEST)
    
    if default_token_generator.check_token(user, token):
        user.set_password(new_password)
        user.save()
        print('user:', user)
        print('user.password:', user.password)
        return Response({"message": "Password reset successful"}, status=status.HTTP_200_OK)
    else:
        return Response({"error": "Invalid or expired token"}, status=status.HTTP_400_BAD_REQUEST)
    

