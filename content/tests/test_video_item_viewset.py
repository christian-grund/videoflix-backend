from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from content.models import VideoItem
from django.core.files.uploadedfile import SimpleUploadedFile
from user.models import CustomUser

User = get_user_model()

class VideoItemViewSetTestCase(APITestCase):
    
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username='testuser', 
            email='testuser@example.com', 
            password='testpassword'
        )
        self.client.force_authenticate(user=self.user)

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
            'video_file': self.dummy_file,  # Dummy-Datei zuweisen
            'has_sound': True,
        }

    def test_create_video_item(self):
        url = reverse('videoitem-list')  
        response = self.client.post(url, self.video_data, format='multipart')  
        self.assertEqual(response.status_code, 201)
        self.assertEqual(VideoItem.objects.count(), 1)
        video_item = VideoItem.objects.first()
        self.assertEqual(video_item.title, 'Test Video Title')
        self.assertEqual(video_item.user, self.user)
    
    def test_list_video_items(self):
        VideoItem.objects.create(
        name='Test Video',
        title='Test Video Title',
        description='Test Video Description',
        categories=['test', 'video'],
        video_file=self.dummy_file,  
        has_sound=True,
        user=self.user
    )

        url = reverse('videoitem-list')  
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1) 
        self.assertEqual(response.data[0]['title'], 'Test Video Title')
        self.assertEqual(response.data[0]['name'], 'Test Video')
    

    def test_delete_video_item(self):
        video_item = VideoItem.objects.create(
        name='Test Video',
        title='Test Video Title',
        description='Test Video Description',
        categories=['test', 'video'],
        video_file=self.dummy_file,  # Dummy-Datei
        has_sound=True,
        user=self.user
        )

        url = reverse('videoitem-detail', args=[video_item.id]) 
        response = self.client.delete(url)

        self.assertEqual(response.status_code, 204)  
        self.assertEqual(VideoItem.objects.count(), 0) 

