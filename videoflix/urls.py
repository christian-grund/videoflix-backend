from django.contrib import admin
from django.urls import path

from auth.register.views import RegisterViewSet

urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('register/', RegisterViewSet.as_view({'post': 'create'}), name='RegisterView'),
]
