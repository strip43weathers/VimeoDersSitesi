from django.db import models
from django.contrib.auth.models import User


class Kurs(models.Model):
    baslik = models.CharField(max_length=200, verbose_name="Kurs Başlığı")
    aciklama = models.TextField(verbose_name="Kurs Açıklaması", blank=True, null=True)
    gorsel = models.ImageField(upload_to='kurs_gorselleri/', blank=True, null=True, verbose_name="Kurs Görseli")
    olusturulma_tarihi = models.DateTimeField(auto_now_add=True)

    herkese_acik = models.BooleanField(default=True, verbose_name="Herkese Açık")
    izinli_kullanicilar = models.ManyToManyField(User, blank=True, related_name='erisilebilen_kurslar', verbose_name="İzinli Kullanıcılar")

    def __str__(self):
        return self.baslik

    class Meta:
        verbose_name = "Kurs"
        verbose_name_plural = "Kurslar"


class Ders(models.Model):

    kurs = models.ForeignKey(Kurs, on_delete=models.CASCADE, related_name='dersler', verbose_name="Ait Olduğu Kurs")
    baslik = models.CharField(max_length=200, verbose_name="Ders Başlığı")
    aciklama = models.TextField(verbose_name="Ders Açıklaması", blank=True, null=True)
    vimeo_video_id = models.CharField(
        max_length=20,
        verbose_name="Vimeo Video ID",
        help_text="Vimeo linkindeki sayıyı girin (örn: 123456789)"
    )
    sira_numarasi = models.PositiveIntegerField(verbose_name="Sıra Numarası", default=0, help_text="Derslerin hangi sırada gösterileceğini belirler.")
    olusturulma_tarihi = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.kurs.baslik} - {self.baslik}"

    class Meta:
        verbose_name = "Ders"
        verbose_name_plural = "Dersler"
        ordering = ['sira_numarasi']
