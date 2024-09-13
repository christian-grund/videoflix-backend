from django.contrib import admin
from content.models import VideoItem

@admin.register(VideoItem)
class VideoItemAdmin(admin.ModelAdmin):
    list_display = ['title']
