# odeme/urls.py

from django.urls import path
from . import views

app_name = 'odeme'

urlpatterns = [
    path('sertifika-sinavi/', views.sinav_bilgilendirme, name='sinav_bilgilendirme'),
    path('sinav-satin-al/', views.sinav_satin_al, name='sinav_satin_al'),
    path('kayit-basarili/', views.kayit_basarili, name='kayit_basarili'),
    path('kayit-mevcut/', views.kayit_mevcut, name='kayit_mevcut'),
    # YENİ EKLENEN SÖZLEŞME URL'İ
    path('satis-sozlesmesi/', views.satis_sozlesmesi, name='satis_sozlesmesi'),
]
