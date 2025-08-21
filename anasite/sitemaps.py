# anasite/sitemaps.py

from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from dersler.models import Kurs
from sayfalar.models import Sayfa

class KursSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.9

    def items(self):
        # SADECE HERKESE AÇIK OLAN VİDEOLARI/KURSLARI LİSTELER
        return Kurs.objects.filter(herkese_acik=True)

    def location(self, obj):
        return reverse('kurs_detay', args=[obj.slug])

class SayfaSitemap(Sitemap):
    changefreq = "yearly"
    priority = 0.5

    def items(self):
        return Sayfa.objects.all()

    def location(self, obj):
        return reverse('sayfa_detay', args=[obj.slug])

class StaticViewSitemap(Sitemap):
    priority = 0.7
    changefreq = 'daily'

    def items(self):
        return ['anasayfa', 'kurs_listesi', 'oyun_listesi']

    def location(self, item):
        return reverse(item)
