# anasite/sitemaps.py

from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from dersler.models import Kurs
from sayfalar.models import Sayfa

class KursSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.9

    def items(self):
        # Sadece 'herkese açık' olan ve slug'ı boş olmayan kursları al
        return Kurs.objects.filter(herkese_acik=True).exclude(slug__exact='')

    def location(self, obj):
        return reverse('kurs_detay', args=[obj.slug])

class SayfaSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.5

    def items(self):
        # Sadece slug'ı boş olmayan sayfaları al
        return Sayfa.objects.exclude(slug__exact='')

    def location(self, obj):
        return reverse('sayfa_detay', args=[obj.slug])

class StaticViewSitemap(Sitemap):
    priority = 0.7
    changefreq = 'daily'

    def items(self):
        return ['anasayfa', 'kurs_listesi', 'oyun_listesi']

    def location(self, item):
        return reverse(item)