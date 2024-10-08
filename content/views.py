from django.shortcuts import render
from django.http import JsonResponse
from django.db import models
from django.db.models import Q
from content.admin import VideoItemResource
from content.models import VideoItem
from content.serializers import VideoItemSerializer
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from django.http import JsonResponse
from django.conf import settings
import os

import logging

logger = logging.getLogger(__name__)

class VideoItemViewSet(viewsets.ModelViewSet):
    queryset = VideoItem.objects.all()
    serializer_class = VideoItemSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]  # IsAuthenticatedOrReadOnly Authentifizierung nicht erforderlich für lesende Zugriffe
    # authentication_classes = []

    def get_queryset(self):
        user = self.request.user

        if user.is_authenticated:
            # Benutzer bekommt seine eigenen Videos und die öffentlichen (user=None) Videos angezeigt
            return VideoItem.objects.filter(models.Q(user=user) | models.Q(user__isnull=True))

        # Nicht authentifizierte Benutzer sehen nur öffentliche Videos (user=None)
        return VideoItem.objects.filter(user__isnull=True)
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if not queryset.exists():
            return Response({'detail': 'No videos found.'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


def check_thumbnail_status(request, video_name):
    print('check_thumbnail_status')
    thumbnail_path = os.path.join(settings.MEDIA_ROOT, 'thumbnails', f'{video_name}_with_text.jpg')
    print(f'Überprüfe Thumbnail-Pfad: {thumbnail_path}')
    
    if os.path.exists(thumbnail_path):
        return JsonResponse({"status": "completed"})
    else:
        return JsonResponse({'status': 'pending'})  
    

def check_convertion_status(request, video_name):
    print('check_convertion_status')
    video_360p_path = os.path.join(settings.MEDIA_ROOT, 'videos', f'{video_name}_360p.mp4')
    video_720p_path = os.path.join(settings.MEDIA_ROOT, 'videos', f'{video_name}_720p.mp4')
    video_1080p_path = os.path.join(settings.MEDIA_ROOT, 'videos', f'{video_name}_1080p.mp4')
    print(f'Überprüfe konvertierte Videos:: {video_360p_path} {video_720p_path} {video_1080p_path}')
    
        # Status für jedes Format prüfen
    status_360p = "completed" if os.path.exists(video_360p_path) else "pending"
    status_720p = "completed" if os.path.exists(video_720p_path) else "pending"
    status_1080p = "completed" if os.path.exists(video_1080p_path) else "pending"

    # Alle Status im JSON-Response zurückgeben
    return JsonResponse({
        "360p_status": status_360p,
        "720p_status": status_720p,
        "1080p_status": status_1080p
    }) 


def export_videoitems_json(request):
    video_item_resource = VideoItemResource()
    dataset = video_item_resource.export()
    return JsonResponse(dataset.json, safe=False)


