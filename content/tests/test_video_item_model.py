
from django.test import TestCase
from content.models import VideoItem
from user.models import CustomUser

class VideoItemModelTestCase(TestCase):
    
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='password123'
        )
        
        self.video_item = VideoItem.objects.create(
            name='Test Video',
            title='Test Video Title',
            description='Test Video Description',
            categories=['test', 'video'],
            video_file='path/to/video.mp4',  
            has_sound=True,
            user=self.user
        )

    def test_video_item_creation(self):
        self.assertEqual(self.video_item.name, 'Test Video')
        self.assertEqual(self.video_item.title, 'Test Video Title')
        self.assertEqual(self.video_item.description, 'Test Video Description')
        self.assertEqual(self.video_item.categories, ['test', 'video'])
        self.assertTrue(self.video_item.has_sound)
        self.assertEqual(self.video_item.user, self.user)

    def test_video_item_string_representation(self):
        self.assertEqual(str(self.video_item), 'Test Video Title')

    def test_video_item_creation_without_user(self):
        video_item_without_user = VideoItem.objects.create(
            name='Test Video Without User',
            title='Test Video Title Without User',
            description='Test Video Description Without User',
            categories=['test'],
            video_file='path/to/video.mp4',  
            has_sound=False
        )
        self.assertIsNone(video_item_without_user.user)
