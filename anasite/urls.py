# anasite/urls.py

from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
from django.views.generic.base import TemplateView
from django.contrib.auth import views as auth_views
from dersler import views as dersler_views
from kullanicilar.forms import CustomPasswordResetForm

urlpatterns = [
    path('admin/', admin.site.urls),
    path(
        "robots.txt",
        TemplateView.as_view(template_name="robots.txt", content_type="text/plain"),
    ),
    path('', dersler_views.anasayfa_view, name='anasayfa'),

    # Uygulama URL'leri
    path('blog/', include('blog.urls')),
    path('kurslar/', include('dersler.urls')),
    path('oyunlar/', include('oyunlar.urls')),
    path('odeme/', include('odeme.urls')),
    path('kullanicilar/', include('kullanicilar.urls')),

    # CKEditor URL'i (Eğer kullanıyorsanız ve sildiyseniz bu satırı açın)
    # path('ckeditor/', include('ckeditor_uploader.urls')),

    # Şifre Sıfırlama İşlemleri
    path(
        'hesaplar/password_reset/',
        auth_views.PasswordResetView.as_view(
            form_class=CustomPasswordResetForm,
            template_name='registration/password_reset_form.html'
        ),
        name='password_reset'
    ),
    path('hesaplar/', include('django.contrib.auth.urls')),

    # Sayfalar en sona
    path('', include('sayfalar.urls')),
]

# --- MEDYA DOSYALARINI SUNMA AYARI ---

if settings.DEBUG:
    # Lokal bilgisayarınızda çalışırken (DEBUG=True)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
else:
    # Render / Canlı ortamda çalışırken (DEBUG=False)
    # Bu ayar, 'Render Persistent Disk' içindeki dosyaların tarayıcıda açılmasını sağlar.
    urlpatterns += [
        re_path(r'^media/(?P<path>.*)$', serve, {
            'document_root': settings.MEDIA_ROOT,
        }),
    ]