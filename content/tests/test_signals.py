from django.test import TestCase
from django_rq import get_queue
from unittest.mock import patch
from content.models import VideoItem
from content.signals import video_pre_save
from django.core.files.uploadedfile import SimpleUploadedFile

class VideoItemSignalTestCase(TestCase):

    def setUp(self):
        self.video_item = VideoItem.objects.create(
        name='Test Video',
        title='Test Video Title',
        description='Test Video Description',
        categories=['test', 'video'],
        video_file=SimpleUploadedFile(
            'test_video.mp4', 
            b'test video content', 
            content_type='video/mp4'
        ),
        has_sound=True,
        )


    @patch('django_rq.get_queue')
    def test_video_pre_save_enqueues_tasks_on_title_change(self, mock_get_queue):
        queue = mock_get_queue.return_value
        
        self.video_item.title = 'New Title'
        self.video_item.save()

        self.assertTrue(queue.enqueue.called)
        self.assertEqual(queue.enqueue.call_count, 3)  

    @patch('django_rq.get_queue')
    def test_video_pre_save_does_not_enqueue_tasks_on_title_same(self, mock_get_queue):
        queue = mock_get_queue.return_value
        
        self.video_item.save()

        queue.enqueue.assert_not_called()

    @patch('django_rq.get_queue')
    def test_video_post_save_enqueues_tasks_on_creation(self, mock_get_queue):
        queue = mock_get_queue.return_value
        
        # Erstelle ein neues VideoItem
        new_video_item = VideoItem.objects.create(
            name='New Video',
            title='New Title',
            description='New Description',
            categories=['new', 'video'],
            video_file='videos/new_test_video.mp4',  # Dummy-Datei oder Pfad
            has_sound=False,
        )

        # Überprüfe, ob die Aufgaben in die Warteschlange eingereiht wurden
        self.assertTrue(queue.enqueue.called)
        self.assertEqual(queue.enqueue.call_count, 6)  # 6 Aufgaben sollten hinzugefügt werden



