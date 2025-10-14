# odeme/urls.py

from django.urls import path
from . import views

app_name = 'odeme'

urlpatterns = [
    # --- Sınav URL'leri ---
    path('sertifika-sinavi/', views.sinav_bilgilendirme, name='sinav_bilgilendirme'),
    path('sinav-satin-al/', views.sinav_satin_al, name='sinav_satin_al'),
    path('kayit-basarili/', views.kayit_basarili, name='kayit_basarili'),
    path('kayit-mevcut/', views.kayit_mevcut, name='kayit_mevcut'),

    # --- Genel URL'ler ---
    path('satis-sozlesmesi/', views.satis_sozlesmesi, name='satis_sozlesmesi'),
    path('teslimat-ve-iade-sartlari/', views.teslimat_iade_sartlari, name='teslimat_iade'),

    # --- Eğitim Paketi URL'leri ---
    path('paket/<int:paket_id>/', views.paket_detay_view, name='paket_detay'),
    path('egitim-paketleri/', views.paket_listesi, name='paket_listesi'),
    path('paket-satin-al/<int:paket_id>/', views.paket_satin_al, name='paket_satin_al'),

    # Yeni Eklenen Paket Yönlendirme URL'leri
    path('paket-kayit-basarili/', views.paket_kayit_basarili, name='paket_kayit_basarili'),
    path('paket-kayit-mevcut/', views.paket_kayit_mevcut, name='paket_kayit_mevcut'),

    # --- KİTAP URL'LERİ ---
    path('kitap/<int:kitap_id>/', views.kitap_detay_view, name='kitap_detay'),
    path('kitaplar/', views.kitap_listesi, name='kitap_listesi'),
    path('kitap-satin-al/<int:kitap_id>/', views.kitap_satin_al, name='kitap_satin_al'),
    path('kitap-kayit-basarili/', views.kitap_kayit_basarili, name='kitap_kayit_basarili'),
    path('kitap-kayit-mevcut/', views.kitap_kayit_mevcut, name='kitap_kayit_mevcut'),
]
