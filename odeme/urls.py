# odeme/urls.py

from django.urls import path
from . import views

app_name = 'odeme'

urlpatterns = [
    # --- SEPET İŞLEMLERİ ---
    path('sepet/', views.sepeti_goruntule, name='sepeti_goruntule'),
    path('sepete-ekle/<int:kitap_id>/', views.sepete_ekle, name='sepete_ekle'),
    path('sepetten-cikar/<int:urun_id>/', views.sepetten_cikar, name='sepetten_cikar'),
    path('sepet-guncelle/<int:urun_id>/<str:islem>/', views.sepet_adet_guncelle, name='sepet_adet_guncelle'),

    # --- ÖDEME ---
    path('odeme-yap/', views.odeme_yap, name='odeme_yap'),

    # --- KİTAP URL'LERİ ---
    path('kitap/<int:kitap_id>/', views.kitap_detay_view, name='kitap_detay'),
    path('kitaplar/', views.kitap_listesi, name='kitap_listesi'),

    # --- STATİK SAYFALAR ---
    path('satis-sozlesmesi/', views.satis_sozlesmesi, name='satis_sozlesmesi'),
    path('teslimat-ve-iade-sartlari/', views.teslimat_iade_sartlari, name='teslimat_iade'),
]
