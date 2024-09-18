from content.tasks import convert_360p, convert_720p, convert_1080p

from .models import VideoItem
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
import django_rq
import os


# sender: von welcher Instanz gesendet wurde
# instance: die Instanz selber (z.B. Video-Objekt mit Titel, Description, Datei)
# created: Boolean
# **kwargs:

@receiver(post_save, sender=VideoItem)
def video_post_save(sender, instance, created, **kwargs):
    print('Video wurde gespeichert.')
    if created:
        print('New video created')
        queue = django_rq.get_queue('default', autocommit=True)
        queue.enqueue(convert_360p, instance.video_file.path)
        queue.enqueue(convert_720p, instance.video_file.path)
        queue.enqueue(convert_1080p, instance.video_file.path)

        

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