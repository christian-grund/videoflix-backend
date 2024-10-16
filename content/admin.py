from django.contrib import admin
from content.models import VideoItem
from import_export import resources
from import_export.admin import ImportExportModelAdmin


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