# dosya: oyunlar/urls.py
from django.urls import path
from . import views

app_name = 'oyunlar'
urlpatterns = [
    # Herkese açık oyunlar sayfası
    path('', views.oyun_listesi, name='oyun_listesi'),
    # Sadece üyelere özel oyunlar sayfası (YENİ)
    path('uyelere-ozel/', views.ozel_oyun_listesi, name='ozel_oyun_listesi'),
]
