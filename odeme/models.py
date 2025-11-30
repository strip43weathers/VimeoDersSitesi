# odeme/models.py

from django.db import models
from django.contrib.auth.models import User


# --- ÜRÜN MODELLERİ ---

class Kitap(models.Model):
    baslik = models.CharField(max_length=200, verbose_name="Kitap Başlığı")
    aciklama = models.TextField(verbose_name="Açıklama", blank=True, null=True)
    fiyat = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Fiyat (TL)")
    fotograf = models.ImageField(upload_to='kitap_kapaklari/', blank=True, null=True, verbose_name="Kitap Kapağı")

    def __str__(self):
        return self.baslik


# Paket modelini şimdilik sadece "ürün" olarak tutuyoruz, siparişini kaldırdık.
class EgitimPaketi(models.Model):
    baslik = models.CharField(max_length=200, verbose_name="Paket Başlığı")
    aciklama = models.TextField(verbose_name="Açıklama", blank=True, null=True)
    fiyat = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Fiyat (TL)")
    fotograf = models.ImageField(upload_to='egitim_paketi_kapaklari/', blank=True, null=True,
                                 verbose_name="Paket Kapağı")

    def __str__(self):
        return self.baslik


# --- SEPET SİSTEMİ (YENİ) ---

class Sepet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Kullanıcı")
    session_key = models.CharField(max_length=40, null=True, blank=True, verbose_name="Oturum Anahtarı")
    olusturulma_tarihi = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Sepet {self.id} ({self.user if self.user else self.session_key})"

    @property
    def toplam_tutar(self):
        return sum(item.toplam_fiyat for item in self.items.all())

    @property
    def urun_sayisi(self):
        return sum(item.adet for item in self.items.all())


class SepetUrunu(models.Model):
    sepet = models.ForeignKey(Sepet, related_name='items', on_delete=models.CASCADE)
    kitap = models.ForeignKey(Kitap, on_delete=models.CASCADE, verbose_name="Kitap")
    adet = models.PositiveIntegerField(default=1, verbose_name="Adet")

    def __str__(self):
        return f"{self.adet} x {self.kitap.baslik}"

    @property
    def toplam_fiyat(self):
        return self.kitap.fiyat * self.adet


# --- SİPARİŞ SİSTEMİ (YENİ) ---

class Siparis(models.Model):
    DURUM_SECENEKLERI = (
        ('hazirlaniyor', 'Hazırlanıyor'),
        ('kargoya_verildi', 'Kargoya Verildi'),
        ('tamamlandi', 'Tamamlandı'),
        ('iptal', 'İptal Edildi'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Kullanıcı")
    ad = models.CharField(max_length=100, verbose_name="Ad")
    soyad = models.CharField(max_length=100, verbose_name="Soyad")
    email = models.EmailField(verbose_name="E-posta")
    telefon = models.CharField(max_length=20, verbose_name="Telefon Numarası")
    adres = models.TextField(verbose_name="Teslimat Adresi")

    toplam_tutar = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Toplam Tutar")
    tarih = models.DateTimeField(auto_now_add=True, verbose_name="Sipariş Tarihi")
    durum = models.CharField(max_length=20, choices=DURUM_SECENEKLERI, default='hazirlaniyor',
                             verbose_name="Sipariş Durumu")
    kargo_takip_no = models.CharField(max_length=100, blank=True, null=True, verbose_name="Kargo Takip No")

    class Meta:
        ordering = ['-tarih']
        verbose_name = "Sipariş"
        verbose_name_plural = "Siparişler"

    def __str__(self):
        return f"Sipariş #{self.id} - {self.user.username}"


class SiparisUrunu(models.Model):
    siparis = models.ForeignKey(Siparis, related_name='items', on_delete=models.CASCADE)
    kitap = models.ForeignKey(Kitap, on_delete=models.CASCADE, verbose_name="Kitap")
    fiyat = models.DecimalField(max_digits=10, decimal_places=2,
                                verbose_name="Satış Fiyatı")  # O anki fiyatı saklamak için
    adet = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.adet} x {self.kitap.baslik}"
