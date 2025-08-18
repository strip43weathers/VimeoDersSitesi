# dosya: sayfalar/models.py
from django.db import models
from ckeditor.fields import RichTextField

class Sayfa(models.Model):
    slug = models.SlugField(unique=True, help_text="Sayfanın URL'de görünecek kimliğidir. Örn: 'hakkimizda'")
    baslik = models.CharField(max_length=200, verbose_name="Sayfa Başlığı")
    icerik = RichTextField(verbose_name="Sayfa İçeriği") # Normal TextField yerine RichTextField kullandık
    guncellenme_tarihi = models.DateTimeField(auto_now=True, verbose_name="Son Güncellenme")

    class Meta:
        verbose_name = "Sayfa"
        verbose_name_plural = "Sayfalar"

    def __str__(self):
        return self.baslik