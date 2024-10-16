from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    """
    Custom user model extending the AbstractUser class.
    Adds additional fields: custom, phone, and address.
    """
    custom = models.CharField(max_length=1000, default='')
    phone = models.CharField(max_length=20, default='')
    address = models.CharField(max_length=150, default='')



