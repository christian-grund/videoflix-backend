import content
from videoflix import settings
from .models import VideoItem
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save, post_delete
from content.tasks import convert_video, create_thumbnail_with_text, create_video_screenshot, delete_original_video, delete_screenshot_with_text

import os
import django_rq

@receiver(pre_save, sender=VideoItem)
def video_pre_save(sender, instance, **kwargs):
    """
    Signal handler that triggers before saving a VideoItem instance. 
    If the title has changed, it enqueues tasks to create a video screenshot 
    and thumbnails with the updated title.
    """
    if instance.pk:
        old_instance = VideoItem.objects.get(pk=instance.pk)

        if old_instance.title != instance.title:
            video_file_name_without_extension = os.path.splitext(os.path.basename(instance.video_file.name))[0]
            thumbnail_directory = os.path.join(settings.MEDIA_ROOT, 'thumbnails')
            screenshot_path = os.path.join(thumbnail_directory, f'{video_file_name_without_extension}.jpg')
            screenshot_with_text_path = os.path.join(thumbnail_directory, f'{video_file_name_without_extension}_with_text.jpg')

            queue = django_rq.get_queue('default', autocommit=True)
            queue.enqueue(create_video_screenshot, instance.video_file.path, screenshot_path)
            queue.enqueue(delete_screenshot_with_text, screenshot_with_text_path)
            queue.enqueue(create_thumbnail_with_text, screenshot_path, instance.title)


@receiver(post_save, sender=VideoItem)
def video_post_save(sender, instance, created, **kwargs):
    """
    Signal handler that triggers after saving a VideoItem instance. 
    If the instance is newly created, it enqueues tasks to generate a screenshot, 
    create thumbnails, convert the video into different resolutions, 
    and delete the original video file.
    """
    video_file_name_without_extension = os.path.splitext(os.path.basename(instance.video_file.name))[0]
    thumbnail_directory = os.path.join(settings.MEDIA_ROOT, 'thumbnails')
    screenshot_path = os.path.join(thumbnail_directory, f'{video_file_name_without_extension}.jpg')        

    if created:
        queue = django_rq.get_queue('default', autocommit=True)
        queue.enqueue(create_video_screenshot, instance.video_file.path, screenshot_path)
        queue.enqueue(create_thumbnail_with_text, screenshot_path, instance.title)
        queue.enqueue(convert_video, instance.video_file.path, '_360p', 'scale=640:360')
        queue.enqueue(convert_video, instance.video_file.path, '_720p', 'scale=1280:720')
        queue.enqueue(convert_video, instance.video_file.path, '_1080p', 'scale=1920:1080')
        queue.enqueue(delete_original_video, instance.video_file.path)
        

@receiver(post_delete, sender=VideoItem)
def video_post_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem when corresponding 'Video' object is deleted.
    """
    if instance.video_file:
        if os.path.isfile(instance.video_file.path):
            os.remove(instance.video_file.path)
        

