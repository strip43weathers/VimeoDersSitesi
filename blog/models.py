from django.db import models
from ckeditor.fields import RichTextField
from django.utils.text import slugify


class BlogYazisi(models.Model):
    baslik = models.CharField(max_length=200, verbose_name="Başlık")
    slug = models.SlugField(unique=True, blank=True, verbose_name="URL Yolu (Otomatik Oluşur)")

    # --- YENİ EKLENEN KISIMLAR BAŞLANGIÇ ---
    gorsel = models.ImageField(upload_to='blog/', blank=True, null=True, verbose_name="Kapak Görseli")

    gorsel_alt_metni = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Görsel Alt Metni (SEO)",
        help_text="Görme engelliler ve Google için görseli anlatan kısa bir cümle."
    )

    seo_title = models.CharField(max_length=200, blank=True, null=True, verbose_name="SEO Başlığı (Google)")
    meta_description = models.TextField(blank=True, null=True, verbose_name="Meta Açıklaması")
    # --- YENİ EKLENEN KISIMLAR BİTİŞ ---

    icerik = RichTextField(verbose_name="İçerik")
    sira_numarasi = models.PositiveIntegerField(default=0, verbose_name="Sıra Numarası")
    olusturulma_tarihi = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.baslik

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.baslik.replace('ı', 'i'))
        super(BlogYazisi, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Blog Yazısı"
        verbose_name_plural = "Blog Yazıları"
        ordering = ['sira_numarasi']
