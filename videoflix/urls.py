from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from auth.views import LoginViewSet, LogoutViewSet, SignUpViewSet
from debug_toolbar.toolbar import debug_toolbar_urls

from content.views import export_videoitems_json

urlpatterns = [
    path('admin/', admin.site.urls),
    path('signup/', SignUpViewSet.as_view({'post': 'create'}), name='SignUpView'),
    path('login/', LoginViewSet.as_view({'post': 'create'}), name='LoginView'),
    path('logout/', LogoutViewSet.as_view({'post': 'create'}), name='LogoutView'),
    path('export-videoitems-json/', export_videoitems_json, name='export_videoitems_json'),
    path('django-rq/', include('django_rq.urls')),

] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT) + debug_toolbar_urls()
