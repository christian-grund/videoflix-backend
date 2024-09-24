from datetime import date
from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField

class VideoItem(models.Model):
    created_at = models.DateField(default=date.today)
    name = models.CharField(max_length=50)
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=500)
    categories = ArrayField(models.CharField(max_length=50), blank=True, null=True)
    video_file = models.FileField(upload_to='videos', blank=True, null=True)

    def __str__(self):
        return self.title




# categories = models.JSONField(default=list, blank=True, null=True)