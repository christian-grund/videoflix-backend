from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from auth.views import LoginViewSet, LogoutViewSet, SignUpViewSet

urlpatterns = [
    path('admin/', admin.site.urls),
    path('signup/', SignUpViewSet.as_view({'post': 'create'}), name='SignUpView'),
    path('login/', LoginViewSet.as_view({'post': 'create'}), name='LoginView'),
    path('logout/', LogoutViewSet.as_view({'post': 'create'}), name='LogoutView'),

] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
