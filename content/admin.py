from django.contrib import admin
from content.models import VideoItem
from import_export import resources
from import_export.admin import ImportExportModelAdmin


class VideoItemResource(resources.ModelResource):
    class Meta:
        model = VideoItem  

@admin.register(VideoItem)
class VideoItemAdmin(ImportExportModelAdmin):
    list_display = ['title']