from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from auth.views import ActivateAccountView, LoginViewSet, LogoutViewSet, PasswordResetConfirm, PasswordResetRequest, SignUpViewSet, UserCheckViewSet
from debug_toolbar.toolbar import debug_toolbar_urls
from rest_framework.routers import DefaultRouter
from content.views import VideoItemViewSet, check_convertion_status, check_thumbnail_status

from content.views import export_videoitems_json

router = DefaultRouter()
router.register(r'videos', VideoItemViewSet, basename='videoitem')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('signup/', SignUpViewSet.as_view({'post': 'create'}), name='SignUpView'),
    path('login/', LoginViewSet.as_view({'post': 'create'}), name='LoginView'),
    path('logout/', LogoutViewSet.as_view({'post': 'create'}), name='LogoutView'),
    path('activate/', ActivateAccountView, name='activate-account'),
    path('password-reset/', PasswordResetRequest, name='password_reset_request'),
    path('password-reset-confirm/', PasswordResetConfirm, name='password_reset_confirm'),
    path('api/users/check-email/', UserCheckViewSet.as_view({'get': 'list'}), name='check-email'),
    path('check-thumbnail-status/<str:video_name>/', check_thumbnail_status, name='check_thumbnail_status'),
    path('check-convertion-status/<str:video_name>/', check_convertion_status, name='check_convertion_status'),
    path('export-videoitems-json/', export_videoitems_json, name='export_videoitems_json'),
    path('api/', include(router.urls)),
    path('django-rq/', include('django_rq.urls')),

] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT) + debug_toolbar_urls()
