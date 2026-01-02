# blog/models.py
from django.db import models
from ckeditor.fields import RichTextField
from django.utils.text import slugify


class BlogYazisi(models.Model):
    baslik = models.CharField(max_length=200, verbose_name="Başlık")
    slug = models.SlugField(unique=True, blank=True, verbose_name="URL Yolu (Otomatik Oluşur)")
    icerik = RichTextField(verbose_name="İçerik")
    sira_numarasi = models.PositiveIntegerField(default=0, verbose_name="Sıra Numarası")
    olusturulma_tarihi = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.baslik

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.baslik.replace('ı', 'i'))  # Basit bir Türkçe karakter düzeltmesi
        super(BlogYazisi, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Blog Yazısı"
        verbose_name_plural = "Blog Yazıları"
        ordering = ['sira_numarasi']
