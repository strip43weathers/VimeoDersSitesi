# kullanicilar/apps.py
from django.apps import AppConfig

class KullanicilarConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'kullanicilar'

    def ready(self):
        import kullanicilar.signals
