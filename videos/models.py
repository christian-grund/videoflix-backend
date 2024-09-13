from django.db import models
from django.contrib.auth.models import User

class VideoItem(models.Model):
    name = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    categories = models.JSONField(default=list, blank=True, null=True)

    def __str__(self):
        return self.name

