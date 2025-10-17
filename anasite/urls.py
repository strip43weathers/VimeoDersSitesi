# anasite/urls.py

from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import TemplateView
from dersler import views as dersler_views
from django.contrib.auth import views as auth_views
from kullanicilar.forms import CustomPasswordResetForm

# --- GEREKLİ İMPORTLARI EKLEYİN ---
from django.conf import settings
from django.urls import re_path
from django.views.static import serve
# ------------------------------------

urlpatterns = [
    path('admin/', admin.site.urls),
    path(
        "robots.txt",
        TemplateView.as_view(template_name="robots.txt", content_type="text/plain"),
    ),
    path('', dersler_views.anasayfa_view, name='anasayfa'),
    path('blog/', include('blog.urls')),
    #       path('kitap-kayit/', include('kitapkayit.urls')),
    path('kurslar/', include('dersler.urls')),
    path('oyunlar/', include('oyunlar.urls')),
    path('odeme/', include('odeme.urls')),
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
    path('', include('sayfalar.urls')),
]

# --- CANLI ORTAMDA MEDYA DOSYALARINI SUNMAK İÇİN BU SATIRI EKLEYİN ---
# Bu satır, /media/ ile başlayan URL'leri MEDIA_ROOT klasörünüzle eşleştirir.
urlpatterns += [re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT})]
