from rest_framework import serializers
from content.models import VideoItem

class VideoItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoItem
        fields = '__all__'
        read_only_fields = ['user']

    def create(self, validated_data):
        # den eingeloggten User zu den Videodaten hinzufügen
        validated_data['user'] = self.context['request'].user if self.context['request'].user.is_authenticated else None
        return super().create(validated_data)
    
    
