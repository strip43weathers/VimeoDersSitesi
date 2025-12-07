# dosya: sayfalar/models.py
from django.db import models
from ckeditor.fields import RichTextField

class Sayfa(models.Model):
    slug = models.SlugField(unique=True, help_text="Sayfanın URL'de görünecek kimliğidir. Örn: 'hakkimizda'")
    baslik = models.CharField(max_length=200, verbose_name="Sayfa Başlığı")
    icerik = RichTextField(verbose_name="Sayfa İçeriği")
    guncellenme_tarihi = models.DateTimeField(auto_now=True, verbose_name="Son Güncellenme")

    class Meta:
        verbose_name = "Sayfa"
        verbose_name_plural = "Sayfalar"

    def __str__(self):
        return self.baslik

class RehberVideo(models.Model):
    # SAYFA SEÇENEKLERİNİ Tanimlayalim
    SAYFA_SECENEKLERI = [
        ('anasayfa', 'Ana Sayfa'),
        ('blog', 'Blog Sayfası'),
    ]

    sayfa = models.CharField(
        max_length=10,
        choices=SAYFA_SECENEKLERI,
        default='anasayfa',
        verbose_name="Görüneceği Sayfa"
    )
    baslik = models.CharField(max_length=200, verbose_name="Rehber Video Başlığı")
    vimeo_video_id = models.CharField(
        max_length=20,
        verbose_name="Vimeo Video ID",
        help_text="Vimeo linkindeki sayıyı girin (örn: 123456789)"
    )
    aktif = models.BooleanField(default=True, verbose_name="Bu Video Aktif mi?")

    class Meta:
        verbose_name = "Rehber Videosu"
        verbose_name_plural = "Rehber Videoları"

    def __str__(self):
        # Hangi sayfaya ait olduğunu admin panelinde daha net görelim
        return f"{self.get_sayfa_display()} - {self.baslik}"


# sayfalar/models.py dosyasına ekleyin:

class IletisimTalebi(models.Model):
    ad_soyad = models.CharField(max_length=100, verbose_name="Ad Soyad")
    email = models.EmailField(verbose_name="E-posta Adresi")
    telefon = models.CharField(max_length=20, verbose_name="Telefon Numarası")
    mesaj = models.TextField(verbose_name="Mesaj", blank=True, null=True) # İsteğe bağlı mesaj alanı
    olusturulma_tarihi = models.DateTimeField(auto_now_add=True, verbose_name="Tarih")

    class Meta:
        verbose_name = "İletişim Talebi"
        verbose_name_plural = "İletişim Talepleri"
        ordering = ['-olusturulma_tarihi']

    def __str__(self):
        return f"{self.ad_soyad} - {self.telefon}"