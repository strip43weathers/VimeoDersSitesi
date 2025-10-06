# anasite/urls.py

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic.base import TemplateView
from dersler import views as dersler_views
from django.contrib.auth import views as auth_views
from kullanicilar.forms import CustomPasswordResetForm

urlpatterns = [
    path('admin/', admin.site.urls),
    path(
        "robots.txt",
        TemplateView.as_view(template_name="robots.txt", content_type="text/plain"),
    ),
    path('', dersler_views.anasayfa_view, name='anasayfa'),
    path('blog/', include('blog.urls')),
    path('kitap-kayit/', include('kitapkayit.urls')),
    path('kurslar/', include('dersler.urls')),
    path('oyunlar/', include('oyunlar.urls')),
    path('kullanicilar/', include('kullanicilar.urls')),
    path(
        'hesaplar/password_reset/',
        auth_views.PasswordResetView.as_view(
            form_class=CustomPasswordResetForm,
            template_name='registration/password_reset_form.html'
        ),
        name='password_reset'
    ),
    path('hesaplar/', include('django.contrib.auth.urls')),
    # DİKKAT: Bu genel yakalayıcı (catch-all) en sona yakın olmalı
    path('', include('sayfalar.urls')),
]

# Medya dosyalarının geliştirme ortamında sunulması için URL desenini listenin SONUNA ekleyin.
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
