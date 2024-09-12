from django.contrib import admin
from django.urls import path

from auth.register.views import LoginViewSet, LogoutViewSet, RegisterViewSet

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', RegisterViewSet.as_view({'post': 'create'}), name='RegisterView'),
    path('login/', LoginViewSet.as_view({'post': 'create'}), name='LoginView'),
    path('logout/', LogoutViewSet.as_view({'post': 'create'}), name='LogoutView'),
]
