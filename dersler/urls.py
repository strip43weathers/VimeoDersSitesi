from django.urls import path
from . import views

app_name = 'dersler' # Bu, URL'leri isimlendirirken karışıklığı önler

urlpatterns = [
    # /dersler/ -> Bütün kursların listesi
    path('', views.kurs_listesi, name='kurs_listesi'),

    # /dersler/1/ -> 1 ID'li kursun detay sayfası (dersleri listeler)
    path('<int:kurs_id>/', views.kurs_detay, name='kurs_detay'),

    # /dersler/1/ders/5/ -> 1 ID'li kursun 5 ID'li dersinin sayfası (videoyu gösterir)
    path('<int:kurs_id>/ders/<int:ders_id>/', views.ders_detay, name='ders_detay'),
]