from django.apps import AppConfig

class DbConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'db'

    def ready(self):
        from . import signals  # Import the signals inside the ready method
