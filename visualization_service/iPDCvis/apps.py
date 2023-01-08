from django.apps import AppConfig


class IpdcvisConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'iPDCvis'

    def ready(self):
        from .data_bridge import listenToPort
        listenToPort()