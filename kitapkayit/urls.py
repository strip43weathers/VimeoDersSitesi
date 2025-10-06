# kitapkayit/urls.py
from django.urls import path
from . import views

app_name = 'kitapkayit'

urlpatterns = [
    path('', views.kitap_kayit_view, name='kayit_formu'),
    path('basarili/', views.kayit_basarili_view, name='kayit_basarili'),
]
