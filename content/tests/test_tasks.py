from unittest.mock import patch, MagicMock
from django.test import TestCase
import subprocess
import os

from content.tasks import convert_video, create_thumbnail_with_text, create_video_screenshot, delete_original_screenshot, delete_original_video, delete_screenshot_with_text

class ConvertVideoTests(TestCase):

    @patch('subprocess.run')
    @patch('os.path.exists', return_value=True)  
    def test_convert_video_calls_ffmpeg(self, mock_exists, mock_run):
        source = './media/videos/ai.mp4'
        resolution = '_720p'
        scale = 'scale=1280:720'

        convert_video(source, resolution, scale)

        expected_cmd = '/Users/christian/usr/ffmpeg/ffmpeg -i "{}" -vf {} -c:v libx264 -crf 23 -c:a aac -strict -2 "{}"'.format(source, scale, './media/videos/ai_720p.mp4')
        mock_run.assert_called_once_with(expected_cmd, shell=True)


    @patch('subprocess.run')
    def test_convert_video_with_invalid_source(self, mock_run):
        source = '/invalid/path/to/video.mp4'  
        resolution = '_720p'
        scale = 'scale=1280:720'

        with self.assertRaises(FileNotFoundError) as context:
            convert_video(source, resolution, scale)

        self.assertEqual(str(context.exception), f"Source file '{source}' does not exist.")

        mock_run.assert_not_called()


class CreateVideoScreenshotTests(TestCase):

    @patch('subprocess.run')
    def test_create_video_screenshot_calls_ffmpeg(self, mock_run):
        video_path = 'media/videos/ai.mp4'
        output_image_path = '/path/to/output_image.jpg'
        time = '00:00:05'
        
        with patch('os.path.exists') as mock_exists:
            mock_exists.side_effect = [True, False]  
            
            create_video_screenshot(video_path, output_image_path, time)

            expected_command = [
                'ffmpeg',
                '-ss', time,
                '-i', video_path,
                '-vframes', '1',
                '-q:v', '2',
                output_image_path
            ]
            mock_run.assert_called_once_with(expected_command, check=True)


class DeleteOriginalVideoTests(TestCase):

    @patch('os.path.isfile')
    @patch('os.remove')
    def test_delete_original_video_calls_remove(self, mock_remove, mock_isfile):
        video_path = '/media/videos/ai.mp4'
        
        mock_isfile.return_value = True

        delete_original_video(video_path)

        mock_remove.assert_called_once_with(video_path)


class DeleteOriginalScreenshotTests(TestCase):

    @patch('os.path.isfile')
    @patch('os.remove')
    def test_delete_original_screenshot_calls_remove(self, mock_remove, mock_isfile):
        screenshot_path = 'media/thumbnails/ai.jpg'
        
        mock_isfile.return_value = True

        delete_original_screenshot(screenshot_path)

        mock_remove.assert_called_once_with(screenshot_path)


class DeleteScreenshotWithTextTests(TestCase):

    @patch('os.path.isfile')
    @patch('os.remove')
    def test_delete_screenshot_with_text_calls_remove(self, mock_remove, mock_isfile):
        screenshot_path = 'media/thumbnails/ai_with_text.jpg'
        
        mock_isfile.return_value = True

        delete_screenshot_with_text(screenshot_path)

        mock_remove.assert_called_once_with(screenshot_path)


class CreateThumbnailWithTextTests(TestCase):

    @patch('subprocess.run')
    def test_create_thumbnail_with_text_calls_ffmpeg(self, mock_run):
        image_path = '/path/to/image.jpg'
        video_title = 'Test Video Title'
        
        output_path = create_thumbnail_with_text(image_path, video_title)

        expected_output_path = os.path.splitext(image_path)[0] + '_with_text.jpg'
        self.assertEqual(output_path, expected_output_path)

        expected_command = [
            'ffmpeg',
            '-i', image_path,
            '-vf', f"drawtext=text='{video_title}':fontcolor=white:fontsize=145:x=(w-text_w)/2:y=h-(text_h*1.5)",
            expected_output_path
        ]
        mock_run.assert_called_once_with(expected_command, check=True)