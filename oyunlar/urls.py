from django.urls import path
from . import views

app_name = 'oyunlar'
urlpatterns = [

    path('', views.oyun_listesi, name='oyun_listesi'),
    path('uyelere-ozel/', views.ozel_oyun_listesi, name='ozel_oyun_listesi'),
]
