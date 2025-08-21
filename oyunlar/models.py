from django.db import models


class Oyun(models.Model):
    baslik = models.CharField(max_length=200, verbose_name="Oyun Başlığı")
    aciklama = models.TextField(verbose_name="Kısa Açıklama", blank=True, null=True)
    embed_kodu = models.TextField(verbose_name="Oyun Gömme Kodu (iframe)")
    sira_numarasi = models.PositiveIntegerField(default=0, verbose_name="Sıra Numarası")

    sadece_uyelere_ozel = models.BooleanField(
        default=False,
        verbose_name="Sadece Üyelere Özel mi?"
    )

    class Meta:
        verbose_name = "Oyun"
        verbose_name_plural = "Oyunlar"
        ordering = ['sira_numarasi']

    def __str__(self):
        return self.baslik
