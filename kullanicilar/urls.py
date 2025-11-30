from django.urls import path
from . import views

app_name = 'kullanicilar'
urlpatterns = [
    path('kayit/', views.kayit_view, name='kayit'),
    path('hesabim/', views.hesabim_view, name='hesabim'),
]
