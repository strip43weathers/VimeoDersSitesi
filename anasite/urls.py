from django.contrib import admin
from django.urls import path, include

# YENİ: anasayfa_view'ı dersler uygulamasından import ediyoruz
from dersler import views as dersler_views

urlpatterns = [
    # YENİ: Ana sayfa için URL deseni. Boş tırnak ('') ana adresi temsil eder.
    path('', dersler_views.anasayfa_view, name='anasayfa'),

    path('admin/', admin.site.urls),
    path('dersler/', include('dersler.urls')),
    path('hesaplar/', include('django.contrib.auth.urls')),
    path('kullanicilar/', include('kullanicilar.urls')),
]
