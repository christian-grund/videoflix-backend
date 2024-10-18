from django.test import TestCase
from django.urls import reverse
from django.conf import settings
import os

class CheckThumbnailStatusTestCase(TestCase):
    
    def setUp(self):
        self.video_name = 'test_video'
        self.thumbnail_path = os.path.join(settings.MEDIA_ROOT, 'thumbnails', f'{self.video_name}_with_text.jpg')

        if os.path.exists(self.thumbnail_path):
            os.remove(self.thumbnail_path)


    def test_thumbnail_status_pending(self):
        response = self.client.get(reverse('check_thumbnail_status', args=[self.video_name]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['status'], 'pending')
    

    def test_thumbnail_status_completed(self):
        os.makedirs(os.path.dirname(self.thumbnail_path), exist_ok=True)
        with open(self.thumbnail_path, 'w') as f:
            f.write('thumbnail')

        response = self.client.get(reverse('check_thumbnail_status', args=[self.video_name]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['status'], 'completed')

    
