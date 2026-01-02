from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.blog_listesi_view, name='blog_listesi'),
    path('<slug:slug>/', views.blog_detay_view, name='blog_detay'),
]
