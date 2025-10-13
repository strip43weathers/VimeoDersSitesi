# odeme/models.py

from django.db import models
from django.contrib.auth.models import User

class Sinav(models.Model):
    baslik = models.CharField(max_length=200, default="Sertifika Sınavı")
    fiyat = models.DecimalField(max_digits=10, decimal_places=2, default=150.00, verbose_name="Fiyat (EURO)")

    def __str__(self):
        return self.baslik

class SinavSiparisi(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Kullanıcı")
    sinav = models.ForeignKey(Sinav, on_delete=models.CASCADE, verbose_name="Sınav")
    ad = models.CharField(max_length=100, verbose_name="Ad")
    soyad = models.CharField(max_length=100, verbose_name="Soyad")
    email = models.EmailField(verbose_name="E-posta")
    telefon = models.CharField(max_length=20, verbose_name="Telefon Numarası")
    adres = models.TextField(verbose_name="Adres")
    tarih = models.DateTimeField(auto_now_add=True)
    odeme_tamamlandi = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.sinav.baslik}"
