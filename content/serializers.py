from rest_framework import serializers
from content.models import VideoItem

class VideoItemSerializer(serializers.ModelSerializer):
    class Meta:
        """
        Meta class defining the model to be serialized, 
        including all fields and marking 'user' as read-only.
        """
        model = VideoItem
        fields = '__all__'
        read_only_fields = ['user']

    def create(self, validated_data):
        """
        Overrides the create method to associate the authenticated user 
        with the VideoItem if available.
        """
        validated_data['user'] = self.context['request'].user if self.context['request'].user.is_authenticated else None
        return super().create(validated_data)
    
    
