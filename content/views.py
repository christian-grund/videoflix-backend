from django.shortcuts import render
from django.http import JsonResponse
from content.admin import VideoItemResource

def export_videoitems_json(request):
    # Erzeuge eine Instanz der VideoItemResource
    video_item_resource = VideoItemResource()

    # Exportiere die Daten als JSON
    dataset = video_item_resource.export()

    # Füge den JSON-Inhalt zur Response hinzu
    return JsonResponse(dataset.json, safe=False)

