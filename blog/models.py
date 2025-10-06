# blog/models.py
from django.db import models
from ckeditor.fields import RichTextField

class BlogYazisi(models.Model):
    baslik = models.CharField(max_length=200, verbose_name="Başlık")
    icerik = RichTextField(verbose_name="İçerik")
    sira_numarasi = models.PositiveIntegerField(default=0, verbose_name="Sıra Numarası")
    olusturulma_tarihi = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.baslik

    class Meta:
        verbose_name = "Blog Yazısı"
        verbose_name_plural = "Blog Yazıları"
        ordering = ['sira_numarasi']
