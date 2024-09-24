from videoflix import settings
from .models import VideoItem
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
import django_rq

from content.tasks import convert_video, create_thumbnail_with_text, create_video_screenshot, delete_original_screenshot, delete_original_video
import os



# sender: von welcher Instanz gesendet wurde
# instance: die Instanz selber (z.B. Video-Objekt mit Titel, Description, Datei)
# created: Boolean
# **kwargs:

@receiver(post_save, sender=VideoItem)
def video_post_save(sender, instance, created, **kwargs):
    print('Video wurde gespeichert.')
    video_file_name_without_extension = os.path.splitext(os.path.basename(instance.video_file.name))[0]
    thumbnail_directory = os.path.join(settings.MEDIA_ROOT, 'thumbnails')
    screenshot_path = os.path.join(thumbnail_directory, f'{video_file_name_without_extension}.jpg')        

    if created:
        print('New video created')
        queue = django_rq.get_queue('default', autocommit=True)
        queue.enqueue(convert_video, instance.video_file.path, '_360p', 'scale=640:360')
        queue.enqueue(convert_video, instance.video_file.path, '_720p', 'scale=1280:720')
        queue.enqueue(convert_video, instance.video_file.path, '_1080p', 'scale=1920:1080')
        queue.enqueue(create_video_screenshot, instance.video_file.path, screenshot_path)
        queue.enqueue(create_thumbnail_with_text, screenshot_path, instance.title)
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




# pre: davor, post: danach
# pre_delete und post_delete auch möglich
# diese Art der Registrierung ist veraltet
# post_save.connect(video_post_save, sender=VideoItem)