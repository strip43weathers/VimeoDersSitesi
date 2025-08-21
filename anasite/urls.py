from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic.base import TemplateView
from dersler import views as dersler_views

# Sitemap için gerekli import'lar
from django.contrib.sitemaps.views import sitemap
from .sitemaps import KursSitemap, OyunSitemap, SayfaSitemap, StaticViewSitemap

from django.contrib.auth import views as auth_views
from kullanicilar.forms import CustomPasswordResetForm

# sitemaps sözlüğünü oluşturun
sitemaps = {
    'kurslar': KursSitemap,
    'oyunlar': OyunSitemap,
    'sayfalar': SayfaSitemap,
    'static': StaticViewSitemap,
}

urlpatterns = [
    path('admin/', admin.site.urls),

    # Sitemap ve robots.txt URL'leri
    path(
        "sitemap.xml",
        sitemap,
        {"sitemaps": sitemaps},
        name="django.contrib.sitemaps.views.sitemap",
    ),
    path(
        "robots.txt",
        TemplateView.as_view(template_name="robots.txt", content_type="text/plain"),
    ),

    path('', dersler_views.anasayfa_view, name='anasayfa'),

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

    path('', include('sayfalar.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)