from django.contrib import admin
from content.models import VideoItem
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin


@admin.register(User)
class UserAdmin(DefaultUserAdmin):
    list_display = ('id', 'username', 'email', 'is_staff', 'is_active')


class VideoItemResource(resources.ModelResource):
    """
    Represents the resource for importing and exporting VideoItem data.
    """
    class Meta:
        model = VideoItem  


@admin.register(VideoItem)
class VideoItemAdmin(ImportExportModelAdmin):
    """
    Admin interface for managing VideoItem objects with import/export capabilities.
    """
    list_display = ['title']

