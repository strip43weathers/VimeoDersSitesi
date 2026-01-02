from django.shortcuts import render, get_object_or_404
from .models import BlogYazisi
from sayfalar.models import RehberVideo
from django.utils.text import Truncator


def blog_listesi_view(request):
    # Tüm blog yazılarını çek
    yazilar = BlogYazisi.objects.all()

    # Her yazı için kısa bir özet oluştur (Listeleme sayfasında göstermek için)
    for yazi in yazilar:
        yazi.ozet = Truncator(yazi.icerik).words(30, html=True, truncate='...')

    # 'blog' sayfası için aktif olan TÜM videoları çek (Üst kısımdaki akordiyon için)
    rehber_videolar = RehberVideo.objects.filter(aktif=True, sayfa='blog')

    context = {
        'yazilar': yazilar,
        'rehber_videolar': rehber_videolar
    }
    return render(request, 'blog/blog_listesi.html', context)


def blog_detay_view(request, slug):
    # URL'den gelen slug (örn: 'python-dersleri') ile veritabanındaki yazıyı bul
    # Eğer böyle bir yazı yoksa 404 Sayfa Bulunamadı hatası ver
    yazi = get_object_or_404(BlogYazisi, slug=slug)

    context = {
        'yazi': yazi
    }
    return render(request, 'blog/blog_detay.html', context)