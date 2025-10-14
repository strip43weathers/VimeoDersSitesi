# odeme/models.py

from django.db import models
from django.contrib.auth.models import User

# --- MEVCUT MODELLERİNİZ ---
class Sinav(models.Model):
    baslik = models.CharField(max_length=200, default="Sertifika Sınavı")
    fiyat = models.DecimalField(max_digits=10, decimal_places=2, default=150.00, verbose_name="Fiyat (EURO)")

    def __str__(self):
        return self.baslik

class SinavSiparisi(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Kullanıcı")
    sinav = models.ForeignKey(Sinav, on_delete=models.CASCADE, verbose_name="Sınav")
    tarih = models.DateTimeField(auto_now_add=True)
    odeme_tamamlandi = models.BooleanField(default=False)
    # Önceki isteğinizde eklediğimiz alanları da burada tutuyoruz.
    ad = models.CharField(max_length=100, verbose_name="Ad", blank=True, null=True)
    soyad = models.CharField(max_length=100, verbose_name="Soyad", blank=True, null=True)
    email = models.EmailField(verbose_name="E-posta", blank=True, null=True)
    telefon = models.CharField(max_length=20, verbose_name="Telefon Numarası", blank=True, null=True)
    adres = models.TextField(verbose_name="Adres", blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.sinav.baslik}"

# --- YENİ EKLENEN MODELLER ---
class EgitimPaketi(models.Model):
    baslik = models.CharField(max_length=200, verbose_name="Paket Başlığı")
    aciklama = models.TextField(verbose_name="Açıklama", blank=True, null=True)
    fiyat = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Fiyat (EURO)")

    def __str__(self):
        return self.baslik

class PaketSiparisi(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Kullanıcı")
    paket = models.ForeignKey(EgitimPaketi, on_delete=models.CASCADE, verbose_name="Eğitim Paketi")
    ad = models.CharField(max_length=100, verbose_name="Ad")
    soyad = models.CharField(max_length=100, verbose_name="Soyad")
    email = models.EmailField(verbose_name="E-posta")
    telefon = models.CharField(max_length=20, verbose_name="Telefon Numarası")
    adres = models.TextField(verbose_name="Adres")
    tarih = models.DateTimeField(auto_now_add=True)
    odeme_tamamlandi = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.paket.baslik}"


class Kitap(models.Model):
    baslik = models.CharField(max_length=200, verbose_name="Kitap Başlığı")
    aciklama = models.TextField(verbose_name="Açıklama", blank=True, null=True)
    fiyat = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Fiyat (EURO)")
    # Yeni eklenen alan
    fotograf = models.ImageField(upload_to='kitap_kapaklari/', blank=True, null=True, verbose_name="Kitap Kapağı")

    def __str__(self):
        return self.baslik


class KitapSiparisi(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Kullanıcı")
    kitap = models.ForeignKey(Kitap, on_delete=models.CASCADE, verbose_name="Kitap")
    ad = models.CharField(max_length=100, verbose_name="Ad")
    soyad = models.CharField(max_length=100, verbose_name="Soyad")
    email = models.EmailField(verbose_name="E-posta")
    telefon = models.CharField(max_length=20, verbose_name="Telefon Numarası")
    adres = models.TextField(verbose_name="Adres")
    tarih = models.DateTimeField(auto_now_add=True)
    odeme_tamamlandi = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.kitap.baslik}"