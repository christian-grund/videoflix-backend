from django.apps import AppConfig


class ContentConfig(AppConfig):
    """
    Configuration class for the 'content' Django app, 
    setting default auto field type and importing signals on startup.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'content'

    def ready(self):
        from . import signals
