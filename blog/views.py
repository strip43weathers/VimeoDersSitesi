# dosya: blog/views.py
from django.shortcuts import render
from .models import BlogYazisi
from sayfalar.models import RehberVideo
from django.utils.text import Truncator


def blog_listesi_view(request):
    yazilar = BlogYazisi.objects.all()

    for yazi in yazilar:
        yazi.ozet = Truncator(yazi.icerik).words(30, html=True, truncate='...')

    # 'blog' sayfası için aktif olan TÜM videoları çek
    rehber_videolar = RehberVideo.objects.filter(aktif=True, sayfa='blog')

    context = {
        'yazilar': yazilar,
        'rehber_videolar': rehber_videolar  # Değişken adını çoğul yapıyoruz
    }
    return render(request, 'blog/blog_listesi.html', context)
