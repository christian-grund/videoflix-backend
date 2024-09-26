from django.shortcuts import render
from django.http import JsonResponse
from content.admin import VideoItemResource
from content.models import VideoItem
from content.serializers import VideoItemSerializer
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

import logging

logger = logging.getLogger(__name__)

class VideoItemViewSet(viewsets.ModelViewSet):
    print('VideoItemViewSet')
    queryset = VideoItem.objects.all()
    serializer_class = VideoItemSerializer
    permission_classes = [IsAuthenticated]  # Nur authentifizierte Benutzer haben Zugriff

    def get_queryset(self):
        # Überprüfe, ob der Benutzer authentifiziert ist
        user = self.request.user
        logger.info(f"Anfrage von Benutzer: {user} (Authenticated: {user.is_authenticated})")
        
        if user.is_authenticated:
            logger.info(f"Benutzer ID: {user.id}, Benutzername: {user.username}")
            return VideoItem.objects.filter(user=user)
        
        logger.warning("Benutzer nicht authentifiziert")
        return VideoItem.objects.none()  # Leere Abfrage, wenn kein Benutzer authentifiziert ist

    def list(self, request, *args, **kwargs):
        # Liste der Videos des angemeldeten Benutzers zurückgeben
        queryset = self.get_queryset()
        if not queryset.exists():
            logger.info(f"Keine Videos gefunden für Benutzer {self.request.user.username}")
            return Response({'detail': 'No videos found for this user.'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = self.get_serializer(queryset, many=True)
        logger.info(f"Videos gefunden: {serializer.data}")
        return Response(serializer.data)


def export_videoitems_json(request):
    video_item_resource = VideoItemResource()
    dataset = video_item_resource.export()
    return JsonResponse(dataset.json, safe=False)


