from django.contrib import admin
from django.urls import path, include # include'ü import etmeyi unutma

urlpatterns = [
    path('admin/', admin.site.urls),
    path('dersler/', include('dersler.urls')), # Bu satırı ekliyoruz
    path('hesaplar/', include('django.contrib.auth.urls')),
    path('kullanicilar/', include('kullanicilar.urls')), # Bu satırı ekliyoruz
]
