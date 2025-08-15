from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
# BU SATIRI EKLEYİN
from django.views.generic.base import RedirectView

urlpatterns = [
                  # BU SATIRI EKLEYİN: Ana adrese gelenleri /hesaplar/login/ adresine yönlendirir.
                  path('', RedirectView.as_view(url='/hesaplar/login/', permanent=True)),

                  path('admin/', admin.site.urls),
                  path('dersler/', include('dersler.urls')),
                  path('hesaplar/', include('hesaplar.urls')),
                  path('kullanicilar/', include('kullanicilar.urls')),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
