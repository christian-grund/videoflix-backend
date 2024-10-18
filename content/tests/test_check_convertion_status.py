from django.test import TestCase
from django.urls import reverse
from django.conf import settings
import os

class CheckConvertionStatusTestCase(TestCase):
    
    def setUp(self):
        self.video_name = 'test_video'
        self.video_360p_path = os.path.join(settings.MEDIA_ROOT, 'videos', f'{self.video_name}_360p.mp4')
        self.video_720p_path = os.path.join(settings.MEDIA_ROOT, 'videos', f'{self.video_name}_720p.mp4')
        self.video_1080p_path = os.path.join(settings.MEDIA_ROOT, 'videos', f'{self.video_name}_1080p.mp4')

        if os.path.exists(self.video_360p_path):
            os.remove(self.video_360p_path)
        if os.path.exists(self.video_720p_path):
            os.remove(self.video_720p_path)
        if os.path.exists(self.video_1080p_path):
            os.remove(self.video_1080p_path)

    def test_conversion_status_pending(self):
        response = self.client.get(reverse('check_convertion_status', args=[self.video_name]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['360p_status'], 'pending')
        self.assertEqual(response.json()['720p_status'], 'pending')
        self.assertEqual(response.json()['1080p_status'], 'pending')

    def test_conversion_status_all_completed(self):
        os.makedirs(os.path.dirname(self.video_360p_path), exist_ok=True)
        with open(self.video_360p_path, 'w'), open(self.video_720p_path, 'w'), open(self.video_1080p_path, 'w'):
            pass

        response = self.client.get(reverse('check_convertion_status', args=[self.video_name]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['360p_status'], 'completed')
        self.assertEqual(response.json()['720p_status'], 'completed')
        self.assertEqual(response.json()['1080p_status'], 'completed')

    
