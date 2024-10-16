from django.apps import AppConfig

class DbConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'db'

    # when db app is ready, signals.py listens for events and responds appropriately
    def ready(self):
        from . import signals  # Import the signals inside the ready method
