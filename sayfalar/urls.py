# dosya: sayfalar/urls.py
from django.urls import path
from . import views

app_name = 'sayfalar'
urlpatterns = [
    # Bu yapı <slug>/ şeklinde gelen tüm istekleri yakalayacak. Örn: /hakkimizda/
    path('<slug:slug>/', views.sayfa_detay, name='sayfa_detay'),
]