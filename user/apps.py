from django.apps import AppConfig


class UserConfig(AppConfig):
    """
    Configuration for the user application, 
    defining the name and default field behavior.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'user'
