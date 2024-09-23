from django.shortcuts import render
from django.http import JsonResponse
from content.admin import VideoItemResource
from content.models import VideoItem
from content.serializers import VideoItemSerializer
from rest_framework import viewsets

def export_videoitems_json(request):
    video_item_resource = VideoItemResource()
    dataset = video_item_resource.export()
    return JsonResponse(dataset.json, safe=False)


class VideoItemViewSet(viewsets.ModelViewSet):
    queryset = VideoItem.objects.all()
    serializer_class = VideoItemSerializer