from datetime import date
from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField

class VideoItem(models.Model):
    created_at = models.DateField(default=date.today)
    name = models.CharField(max_length=50)
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=500)
    categories = ArrayField(models.CharField(max_length=50))
    video_file = models.FileField(upload_to='videos')

    def __str__(self):
        return self.title




