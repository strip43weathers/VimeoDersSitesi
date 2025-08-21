# anasite/sitemaps.py

from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from dersler.models import Kurs
from oyunlar.models import Oyun
from sayfalar.models import Sayfa

class KursSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.9

    def items(self):
        # Sadece 'herkese açık' olan kursları site haritasına ekliyoruz.
        return Kurs.objects.filter(herkese_acik=True)

    # Opsiyonel: Kurs modelinize bir güncelleme tarihi alanı eklerseniz
    # bu metodu aktif edebilirsiniz.
    # def lastmod(self, obj):
    #     return obj.guncelleme_tarihi

class OyunSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.8

    def items(self):
        # Sadece 'üyelere özel olmayan' oyunları site haritasına ekliyoruz.
        return Oyun.objects.filter(sadece_uyelere_ozel=False)

class SayfaSitemap(Sitemap):
    changefreq = "yearly"
    priority = 0.5

    def items(self):
        # Sayfa modelinde bir filtreleme alanı olmadığı için hepsini alıyoruz.
        return Sayfa.objects.all()

class StaticViewSitemap(Sitemap):
    priority = 0.7
    changefreq = 'daily'

    def items(self):
        # Bu URL isimleri projenizdeki urls.py dosyalarıyla uyumlu.
        return ['anasayfa', 'kurs_listesi', 'oyun_listesi']

    def location(self, item):
        return reverse(item)
