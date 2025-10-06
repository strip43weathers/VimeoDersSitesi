# blog/urls.py (Yeni oluşturulacak dosya)
from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.blog_listesi_view, name='blog_listesi'),
]
