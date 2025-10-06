# dosya: blog/views.py
from django.shortcuts import render
from .models import BlogYazisi
from sayfalar.models import RehberVideo

def blog_listesi_view(request):
    yazilar = BlogYazisi.objects.all()
    # Sadece blog sayfası için aktif olan videoyu çek
    rehber_video = RehberVideo.objects.filter(aktif=True, sayfa='blog').first()

    context = {
        'yazilar': yazilar,
        'rehber_video': rehber_video
    }
    return render(request, 'blog/blog_listesi.html', context)
