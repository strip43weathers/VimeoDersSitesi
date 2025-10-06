# anasite/wsgi.py

import os
from django.core.wsgi import get_wsgi_application
from django.conf import settings
from whitenoise import WhiteNoise

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'anasite.settings')

# Temel Django uygulamasını al
application = get_wsgi_application()

# WhiteNoise ile sarmala: Önce statik dosyalar için
application = WhiteNoise(application, root=settings.STATIC_ROOT)

# WhiteNoise'a medya dosyalarını da ekle
application.add_files(settings.MEDIA_ROOT, prefix='media/')