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

import logging

logger = logging.getLogger(__name__)

class VideoItemViewSet(viewsets.ModelViewSet):
    queryset = VideoItem.objects.all()
    serializer_class = VideoItemSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]  # Authentifizierung nicht erforderlich für lesende Zugriffe

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



def export_videoitems_json(request):
    video_item_resource = VideoItemResource()
    dataset = video_item_resource.export()
    return JsonResponse(dataset.json, safe=False)


