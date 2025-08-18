from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from dersler import views as dersler_views


from django.contrib.auth import views as auth_views
from kullanicilar.forms import CustomPasswordResetForm

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', dersler_views.anasayfa_view, name='anasayfa'),

    # ÖZEL URL'LERİ GENEL OLANLARDAN ÖNCEYE ALIYORUZ
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

    # EN GENEL URL'İ (TÜM STATİK SAYFALARI KAPSAYAN) EN SONA KOYUYORUZ
    path('', include('sayfalar.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
