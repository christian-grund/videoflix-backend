from datetime import date
from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField

from user.models import CustomUser

class VideoItem(models.Model):
    created_at = models.DateField(default=date.today)
    name = models.CharField(max_length=50)
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=500)
    categories = ArrayField(models.CharField(max_length=50))
    video_file = models.FileField(upload_to='videos')
    has_sound = models.BooleanField(default=False)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='videos', null=True, blank=True)

    def __str__(self):
        return self.title




