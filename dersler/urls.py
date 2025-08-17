from django.urls import path
from . import views

app_name = 'dersler'

urlpatterns = [

    path('', views.kurs_listesi, name='kurs_listesi'),


    path('<int:kurs_id>/', views.kurs_detay, name='kurs_detay'),


    path('<int:kurs_id>/ders/<int:ders_id>/', views.ders_detay, name='ders_detay'),
]
