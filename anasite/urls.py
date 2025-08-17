from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from dersler import views as dersler_views


from django.contrib.auth import views as auth_views
from kullanicilar.forms import CustomPasswordResetForm

urlpatterns = [
    path('', dersler_views.anasayfa_view, name='anasayfa'),
    path('hakkimizda/', dersler_views.hakkimizda_view, name='hakkimizda'),
    path('sss/', dersler_views.sss_view, name='sss'),
    path('gizlilik-politikasi/', dersler_views.gizlilik_view, name='gizlilik'),
    path('kullanim-sartlari/', dersler_views.kullanim_view, name='kullanim'),


    path(
        'hesaplar/password_reset/',
        auth_views.PasswordResetView.as_view(
            form_class=CustomPasswordResetForm,
            template_name='registration/password_reset_form.html'
        ),
        name='password_reset'
    ),

    path('admin/', admin.site.urls),
    path('kurslar/', include('dersler.urls')),


    path('hesaplar/', include('django.contrib.auth.urls')),

    path('kullanicilar/', include('kullanicilar.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
