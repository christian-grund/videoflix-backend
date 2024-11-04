import json
from content.models import VideoItem
from django.urls import reverse
from rest_framework.test import APITestCase
from django.core.files.uploadedfile import SimpleUploadedFile

class ExportVideoItemsJSONTestCase(APITestCase):
    
    def setUp(self):
        self.dummy_file = SimpleUploadedFile(
            'test_video.mp4', 
            b'test video content', 
            content_type='video/mp4'
        )

        self.video_data = {
            'name': 'Test Video',
            'title': 'Test Video Title',
            'description': 'Test Video Description',
            'categories': ['test', 'video'],
            'video_file': self.dummy_file,  
            'has_sound': True,
        }

        self.video_item = VideoItem.objects.create(**self.video_data)

    def test_export_video_items_json(self):
        response = self.client.get(reverse('export_videoitems_json'))
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.content, bytes)
        json_data = response.json()
        self.assertGreater(len(json_data), 0)
