# kitapkayit/models.py
from django.db import models

class KitapKaydi(models.Model):
    isim = models.CharField(max_length=100, verbose_name="İsim")
    soyisim = models.CharField(max_length=100, verbose_name="Soyisim")
    email = models.EmailField(verbose_name="E-posta Adresi")
    telefon = models.CharField(max_length=20, verbose_name="Telefon Numarası")
    kayit_tarihi = models.DateTimeField(auto_now_add=True, verbose_name="Kayıt Tarihi")

    def __str__(self):
        return f"{self.isim} {self.soyisim}"

    class Meta:
        verbose_name = "Kitap Kaydı"
        verbose_name_plural = "Kitap Kayıtları"
        ordering = ['-kayit_tarihi']
