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
from rest_framework.decorators import api_view
from django.http import JsonResponse, Http404
from django.conf import settings
from rest_framework import generics

import os
import logging

logger = logging.getLogger(__name__)

class VideoItemViewSet(viewsets.ModelViewSet):
    """
    Handles CRUD operations for VideoItem instances, allowing authenticated 
    users to manage their videos and providing read-only access to others.
    """
    queryset = VideoItem.objects.all()
    serializer_class = VideoItemSerializer
    permission_classes = [IsAuthenticatedOrReadOnly] 

    def get_queryset(self):
        user = self.request.user

        if user.is_authenticated:
            return VideoItem.objects.filter(models.Q(user=user) | models.Q(user__isnull=True))

        return VideoItem.objects.filter(user__isnull=True)
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if not queryset.exists():
            return Response({'detail': 'No videos found.'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        video_name = instance.name  
        
        self.perform_destroy(instance)

        video_files = [
            os.path.join(settings.MEDIA_ROOT, 'videos', f"{video_name}_360p.mp4"),
            os.path.join(settings.MEDIA_ROOT, 'videos', f"{video_name}_720p.mp4"),
            os.path.join(settings.MEDIA_ROOT, 'videos', f"{video_name}_1080p.mp4"),
            os.path.join(settings.MEDIA_ROOT, 'thumbnails', f"{video_name}.jpg"),
            os.path.join(settings.MEDIA_ROOT, 'thumbnails', f"{video_name}_with_text.jpg")
        ]

        for file_path in video_files:
            if os.path.exists(file_path):
                os.remove(file_path)
                print(f"{file_path} wurde gelöscht.")  
            else:
                print(f"{file_path} nicht gefunden.")  

        return Response(status=status.HTTP_204_NO_CONTENT)


class VideoDetailView(generics.RetrieveAPIView):
    queryset = VideoItem.objects.all()
    serializer_class = VideoItemSerializer

    def get_object(self):
        videoname = self.kwargs['videoname']
        try:
            video_item = VideoItem.objects.get(name=videoname)
            return video_item
        except VideoItem.DoesNotExist:
            raise Http404("Video not found")
        

def check_thumbnail_status(request, video_name):
    """
    Checks if the thumbnail for the specified video exists and returns 
    its status ('completed' or 'pending').
    """
    thumbnail_path = os.path.join(settings.MEDIA_ROOT, 'thumbnails', f'{video_name}_with_text.jpg')
    
    if os.path.exists(thumbnail_path):
        return JsonResponse({"status": "completed"})
    else:
        return JsonResponse({'status': 'pending'})  
    

def check_convertion_status(request, video_name):
    """
    Checks the conversion status of a video for 360p, 720p, and 1080p resolutions 
    and returns their statuses.
    """
    video_360p_path = os.path.join(settings.MEDIA_ROOT, 'videos', f'{video_name}_360p.mp4')
    video_720p_path = os.path.join(settings.MEDIA_ROOT, 'videos', f'{video_name}_720p.mp4')
    video_1080p_path = os.path.join(settings.MEDIA_ROOT, 'videos', f'{video_name}_1080p.mp4')
    
    status_360p = "completed" if os.path.exists(video_360p_path) else "pending"
    status_720p = "completed" if os.path.exists(video_720p_path) else "pending"
    status_1080p = "completed" if os.path.exists(video_1080p_path) else "pending"

    return JsonResponse({
        "360p_status": status_360p,
        "720p_status": status_720p,
        "1080p_status": status_1080p
    })


def export_videoitems_json(request):
    """
    Exports all VideoItem data as JSON and returns it in the response.
    """
    video_item_resource = VideoItemResource()
    dataset = video_item_resource.export()
    return JsonResponse(dataset.json, safe=False)