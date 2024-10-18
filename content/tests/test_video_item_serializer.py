from rest_framework.test import APIRequestFactory, APITestCase
from content.models import VideoItem
from content.serializers import VideoItemSerializer
from user.models import CustomUser
from django.core.files.uploadedfile import SimpleUploadedFile

class VideoItemSerializerTestCase(APITestCase):

    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='password123'
        )

        self.valid_data = {
            'name': 'Test Video',
            'title': 'Test Video Title',
            'description': 'Test Video Description',
            'categories': ['test', 'video'],
            'video_file': SimpleUploadedFile(
                name='test_video.mp4', 
                content=b'test video content', 
                content_type='video/mp4'
            ),
            'has_sound': True,
        }

        # Erstelle ein APIRequestFactory-Objekt
        self.factory = APIRequestFactory()

    def test_video_item_serializer_create_with_user(self):
        request = self.factory.post('/fake-url/', data=self.valid_data)
        request.user = self.user  # Setze den Benutzer

        serializer = VideoItemSerializer(data=self.valid_data, context={'request': request})
        self.assertTrue(serializer.is_valid())
        
        video_item = serializer.save()
        self.assertEqual(video_item.user, self.user)  # Überprüfe, ob der Benutzer korrekt zugewiesen wurde



    def test_video_item_serializer_invalid_data(self):
        invalid_data = self.valid_data.copy()
        invalid_data['name'] = ''  # Ungültiger Name

        request = self.factory.post('/fake-url/', data=invalid_data)
        request.user = self.user  # Simuliere einen authentifizierten Benutzer

        serializer = VideoItemSerializer(data=invalid_data, context={'request': request})
        self.assertFalse(serializer.is_valid())
        self.assertIn('name', serializer.errors)  # Überprüfe, dass ein Fehler für das 'name'-Feld vorhanden ist
