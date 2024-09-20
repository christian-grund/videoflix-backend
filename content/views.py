from django.shortcuts import render
from django.http import JsonResponse
from content.admin import VideoItemResource
from content.models import VideoItem
from content.serializers import VideoItemSerializer
from rest_framework import viewsets

def export_videoitems_json(request):
    # Erzeuge eine Instanz der VideoItemResource
    video_item_resource = VideoItemResource()

    # Exportiere die Daten als JSON
    dataset = video_item_resource.export()

    # Füge den JSON-Inhalt zur Response hinzu
    return JsonResponse(dataset.json, safe=False)


class VideoItemViewSet(viewsets.ModelViewSet):
    queryset = VideoItem.objects.all()
    serializer_class = VideoItemSerializer