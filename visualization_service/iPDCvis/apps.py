from django.apps import AppConfig
import json


class IpdcvisConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'iPDCvis'
    def ready(self):
        from .data_bridge import listenToPort, IDCODE, ALL_CONFIGS
        print("ALL_CONFIGS", json.dumps(ALL_CONFIGS, indent=4))
        listenToPort()
