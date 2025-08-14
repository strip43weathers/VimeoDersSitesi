# anasite/urls.py dosyasının yeni ve son hali
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from kullanicilar.forms import CustomAuthenticationForm

urlpatterns = [
    path('admin/', admin.site.urls),
    path('dersler/', include('dersler.urls')),
    path('', include('kullanicilar.urls')),

    # Standart login view'ını, bizim özel formumuzla birlikte tanımlıyoruz
    path('login/', auth_views.LoginView.as_view(
        template_name='registration/login.html',
        authentication_form=CustomAuthenticationForm  # İşte sihirli kısım!
    ), name='login'),

    # Django'nun logout gibi diğer standart auth URL'lerini dahil et
    path('', include('django.contrib.auth.urls')),
]