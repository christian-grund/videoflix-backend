from rest_framework import serializers
from content.models import VideoItem

class VideoItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoItem
        fields = '__all__'