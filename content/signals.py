from videoflix import settings
from .models import VideoItem
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save, post_delete
from content.tasks import convert_video, create_thumbnail_with_text, create_video_screenshot, delete_original_screenshot, delete_original_video

import os
import django_rq

@receiver(pre_save, sender=VideoItem)
def video_pre_save(sender, instance, **kwargs):
    if instance.pk:
        # Retrieve the old instance before changes are saved
        old_instance = VideoItem.objects.get(pk=instance.pk)
        print(f'Old Instance Title: {old_instance.title}')
        print(f'New Instance Title: {instance.title}')
        
        if old_instance.title != instance.title:
            print('Title changed, updating thumbnail')
            # Delete old thumbnail and create a new one
            queue = django_rq.get_queue('default', autocommit=True)
            video_file_name_without_extension = os.path.splitext(os.path.basename(instance.video_file.name))[0]
            thumbnail_directory = os.path.join(settings.MEDIA_ROOT, 'thumbnails')
            screenshot_path = os.path.join(thumbnail_directory, f'{video_file_name_without_extension}.jpg')
            screenshot_with_text_path = os.path.join(thumbnail_directory, f'{video_file_name_without_extension}_with_text.jpg')

            # Delete old thumbnail with text
            queue.enqueue(delete_original_screenshot, screenshot_with_text_path)

            # Create a new thumbnail with the updated title
            queue.enqueue(create_thumbnail_with_text, screenshot_path, instance.title)


@receiver(post_save, sender=VideoItem)
def video_post_save(sender, instance, created, **kwargs):
    print('Video wurde gespeichert.')
    video_file_name_without_extension = os.path.splitext(os.path.basename(instance.video_file.name))[0]
    thumbnail_directory = os.path.join(settings.MEDIA_ROOT, 'thumbnails')
    screenshot_path = os.path.join(thumbnail_directory, f'{video_file_name_without_extension}.jpg')        
    screenshot_with_text_path = os.path.join(thumbnail_directory, f'{video_file_name_without_extension}_with_text.jpg')        

    if created:
        print('New video created')
        queue = django_rq.get_queue('default', autocommit=True)
        queue.enqueue(create_video_screenshot, instance.video_file.path, screenshot_path)
        queue.enqueue(create_thumbnail_with_text, screenshot_path, instance.title)
        queue.enqueue(convert_video, instance.video_file.path, '_360p', 'scale=640:360')
        queue.enqueue(convert_video, instance.video_file.path, '_720p', 'scale=1280:720')
        queue.enqueue(convert_video, instance.video_file.path, '_1080p', 'scale=1920:1080')
        queue.enqueue(delete_original_video, instance.video_file.path)
        queue.enqueue(delete_original_screenshot, screenshot_path)
        

@receiver(post_delete, sender=VideoItem)
def video_post_delete(sender, instance, **kwargs):
    print('Video wurde gelöscht')
    """
    Deletes file from filesystem when corresponding 'Video' object is deleted.
    """
    if instance.video_file:
        if os.path.isfile(instance.video_file.path):
            os.remove(instance.video_file.path)



# sender: von welcher Instanz gesendet wurde
# instance: die Instanz selber (z.B. Video-Objekt mit Titel, Description, Datei)
# created: Boolean
# **kwargs:
# pre: davor, post: danach
# pre_delete und post_delete auch möglich
# diese Art der Registrierung ist veraltet
# post_save.connect(video_post_save, sender=VideoItem)