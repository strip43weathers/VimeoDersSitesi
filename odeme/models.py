# odeme/models.py

from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings


# --- İNDİRİM KODU SİSTEMİ ---

class IndirimKodu(models.Model):
    kod = models.CharField(max_length=50, unique=True, verbose_name="Kupon Kodu")
    indirim_orani = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(100)],
        verbose_name="İndirim Oranı (%)"
    )
    aktif = models.BooleanField(default=True, verbose_name="Aktif mi?")
    gecerlilik_tarihi = models.DateTimeField(default=timezone.now, verbose_name="Son Kullanma Tarihi")

    # Yeni Eklenen Alanlar
    kullanim_limiti = models.PositiveIntegerField(default=0, verbose_name="Kullanım Limiti (0 = Sınırsız)")
    kullanim_sayisi = models.PositiveIntegerField(default=0, verbose_name="Kullanılma Sayısı")

    def __str__(self):
        return self.kod

    @property
    def gecerli_mi(self):
        # 1. Süre ve aktiflik kontrolü
        zaman_gecerli = self.aktif and self.gecerlilik_tarihi >= timezone.now()

        # 2. Limit kontrolü (0 ise sınırsız demektir)
        limit_gecerli = True
        if self.kullanim_limiti > 0:
            limit_gecerli = self.kullanim_sayisi < self.kullanim_limiti

        return zaman_gecerli and limit_gecerli


# --- ÜRÜN MODELLERİ ---

class Kitap(models.Model):
    baslik = models.CharField(max_length=200, verbose_name="Kitap Başlığı")
    aciklama = models.TextField(verbose_name="Açıklama", blank=True, null=True)
    fiyat = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Fiyat (TL)")
    stok = models.PositiveIntegerField(default=0, verbose_name="Stok Adedi")
    fotograf = models.ImageField(upload_to='kitap_kapaklari/', blank=True, null=True, verbose_name="Kitap Kapağı")
    sira = models.IntegerField(default=0, verbose_name="Sıralama")
    onizleme_dosyasi = models.FileField(
        upload_to='kitap_onizlemeleri/',
        blank=True,
        null=True,
        verbose_name="Önizleme Dosyası (PDF)"
    )

    class Meta:
        ordering = ['sira']

    def __str__(self):
        return self.baslik


class KitapGorsel(models.Model):
    kitap = models.ForeignKey(Kitap, on_delete=models.CASCADE, related_name='ekstra_gorseller')
    gorsel = models.ImageField(upload_to='kitap_detay_gorseller/', verbose_name="Ekstra Görsel")
    sira = models.PositiveIntegerField(default=0, verbose_name="Sıralama")

    class Meta:
        ordering = ['sira']
        verbose_name = "Kitap Görseli"
        verbose_name_plural = "Kitap Görselleri (Galeri)"

    def __str__(self):
        return f"{self.kitap.baslik} - Görsel {self.id}"


class KitapVideo(models.Model):
    kitap = models.ForeignKey(Kitap, on_delete=models.CASCADE, related_name='videolar')
    baslik = models.CharField(max_length=200, verbose_name="Video Başlığı", blank=True)
    dosya = models.FileField(upload_to='kitap_videolar/', verbose_name="Video Dosyası")
    sira = models.PositiveIntegerField(default=0, verbose_name="Sıralama")

    class Meta:
        ordering = ['sira']
        verbose_name = "Kitap Videosu"
        verbose_name_plural = "Kitap Videoları"

    def __str__(self):
        return f"{self.kitap.baslik} - Video {self.baslik}"


# --- SEPET SİSTEMİ ---

class Sepet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Kullanıcı")
    session_key = models.CharField(max_length=40, null=True, blank=True, verbose_name="Oturum Anahtarı")
    olusturulma_tarihi = models.DateTimeField(auto_now_add=True)
    uygulanan_kupon = models.ForeignKey(
        IndirimKodu,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Uygulanan Kupon"
    )

    def __str__(self):
        return f"Sepet {self.id} ({self.user if self.user else self.session_key})"

    @property
    def toplam_tutar(self):
        return sum(item.toplam_fiyat for item in self.items.all())

    @property
    def urun_sayisi(self):
        return sum(item.adet for item in self.items.all())

    @property
    def sepet_son_tutar(self):
        tutar = self.toplam_tutar
        if self.uygulanan_kupon and self.uygulanan_kupon.gecerli_mi:
            indirim_miktari = (tutar * self.uygulanan_kupon.indirim_orani) / 100
            tutar -= indirim_miktari
        return round(tutar, 2)


class SepetUrunu(models.Model):
    sepet = models.ForeignKey(Sepet, related_name='items', on_delete=models.CASCADE)
    kitap = models.ForeignKey(Kitap, on_delete=models.CASCADE, verbose_name="Kitap")
    adet = models.PositiveIntegerField(default=1, verbose_name="Adet")

    def __str__(self):
        return f"{self.adet} x {self.kitap.baslik}"

    @property
    def toplam_fiyat(self):
        return self.kitap.fiyat * self.adet


# --- SİPARİŞ SİSTEMİ ---

class Siparis(models.Model):
    DURUM_SECENEKLERI = (
        ('hazirlaniyor', 'Hazırlanıyor'),
        ('kargoya_verildi', 'Kargoya Verildi'),
        ('tamamlandi', 'Tamamlandı'),
        ('iptal', 'İptal Edildi'),
        ('stok_hatasi', 'Stok Hatası (Ödeme Alındı)'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Kullanıcı")
    ad = models.CharField(max_length=100, verbose_name="Ad")
    soyad = models.CharField(max_length=100, verbose_name="Soyad")
    email = models.EmailField(verbose_name="E-posta")
    telefon = models.CharField(max_length=20, verbose_name="Telefon Numarası")
    tc_kimlik = models.CharField(max_length=11, verbose_name="TC Kimlik No")
    sehir = models.CharField(max_length=50, verbose_name="Şehir")
    posta_kodu = models.CharField(max_length=10, verbose_name="Posta Kodu")
    ulke = models.CharField(max_length=50, verbose_name="Ülke")
    adres = models.TextField(verbose_name="Teslimat Adresi")

    toplam_tutar = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Toplam Tutar")
    tarih = models.DateTimeField(auto_now_add=True, verbose_name="Sipariş Tarihi")
    durum = models.CharField(max_length=20, choices=DURUM_SECENEKLERI, default='hazirlaniyor',
                             verbose_name="Sipariş Durumu")
    kargo_takip_no = models.CharField(max_length=100, blank=True, null=True, verbose_name="Kargo Takip No")
    kullanilan_kupon = models.CharField(max_length=50, blank=True, null=True, verbose_name="Kullanılan Kupon Kodu")

    # --- İYZİCO ENTEGRASYONU İÇİN EKLENEN ALANLAR ---
    odeme_tamamlandi = models.BooleanField(default=False, verbose_name="Ödeme Tamamlandı mı?")
    iyzico_transaction_id = models.CharField(max_length=100, blank=True, null=True, verbose_name="İyzico İşlem ID")

    class Meta:
        ordering = ['-tarih']
        verbose_name = "Sipariş"
        verbose_name_plural = "Siparişler"

    def __str__(self):
        return f"Sipariş #{self.id} - {self.user.username}"

    # --- MAIL VE DURUM GÜNCELLEME SİSTEMİ ---

    def save(self, *args, **kwargs):
        # Sipariş ilk kez oluşturulmuyorsa (güncelleme ise)
        if self.pk:
            try:
                eski_siparis = Siparis.objects.get(pk=self.pk)

                # Durum değişmiş mi kontrol et
                if eski_siparis.durum != self.durum:

                    if self.durum == 'kargoya_verildi':
                        self.mail_kargo_gonder()

                    elif self.durum == 'iptal':
                        self.mail_iptal_gonder()

            except Siparis.DoesNotExist:
                pass

        super().save(*args, **kwargs)

    def mail_kargo_gonder(self):
        subject = f'Siparişiniz Kargoya Verildi - Sipariş No: #{self.id}'
        message = f"""
        Sayın {self.ad} {self.soyad},

        Siparişiniz hazırlanmış ve kargoya verilmiştir.

        Kargo Takip Numaranız: {self.kargo_takip_no if self.kargo_takip_no else 'Takip numarası sisteme girildiğinde ayrıca bildirilecektir.'}

        Bizi tercih ettiğiniz için teşekkür ederiz.
        """
        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [self.email],
            fail_silently=True
        )

    def mail_iptal_gonder(self):
        subject = f'Sipariş İptali Hakkında - Sipariş No: #{self.id}'
        message = f"""
        Sayın {self.ad} {self.soyad},

        Siparişinizi çok üzülerek iptal etmek zorunda kaldık.

        Ödemeniz bankanıza bağlı olarak 3-7 iş günü içerisinde kartınıza iade edilecektir.

        Detaylı bilgi için bizimle iletişime geçebilirsiniz.
        """
        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [self.email],
            fail_silently=True
        )


class SiparisUrunu(models.Model):
    siparis = models.ForeignKey(Siparis, related_name='items', on_delete=models.CASCADE)
    kitap = models.ForeignKey(Kitap, on_delete=models.CASCADE, verbose_name="Kitap")
    fiyat = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Satış Fiyatı")
    adet = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.adet} x {self.kitap.baslik}"