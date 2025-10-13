# dersler/views.py

from django.shortcuts import render, get_object_or_404
from .models import Kurs, Ders
from odeme.models import PaketSiparisi
from blog.models import BlogYazisi  # Hata burada düzeltildi: Post -> BlogYazisi

def anasayfa_view(request):
    """
    Ana sayfayı render eder. Blog yazılarından son 3 tanesini de context'e ekler.
    """
    # Hata burada düzeltildi: Post -> BlogYazisi ve tarih -> olusturulma_tarihi
    recent_posts = BlogYazisi.objects.order_by('-olusturulma_tarihi')[:3]
    return render(request, 'anasayfa.html', {'recent_posts': recent_posts})

def kurs_listesi(request):
    """
    Tüm kursları listeler ve kullanıcının paket sahibi olup olmadığını kontrol eder.
    """
    kurslar = Kurs.objects.all()
    kullanici_paket_sahibi_mi = False
    if request.user.is_authenticated:
        kullanici_paket_sahibi_mi = PaketSiparisi.objects.filter(user=request.user, odeme_tamamlandi=True).exists()

    context = {
        'kurslar': kurslar,
        'kullanici_paket_sahibi_mi': kullanici_paket_sahibi_mi,
    }
    return render(request, 'dersler/kurs_listesi.html', context)

def kurs_detay(request, kurs_id):
    """
    Bir kursun detaylarını ve derslerini gösterir.
    Sadece paket sahibi olan kullanıcılar erişebilir.
    """
    if not request.user.is_authenticated:
        return render(request, 'dersler/erisim_engellendi.html', {'sebep': 'giris_gerekli'})

    if not PaketSiparisi.objects.filter(user=request.user, odeme_tamamlandi=True).exists():
        return render(request, 'dersler/erisim_engellendi.html', {'sebep': 'paket_gerekli'})

    kurs = get_object_or_404(Kurs, pk=kurs_id)
    return render(request, 'dersler/kurs_detay.html', {'kurs': kurs})

def ders_detay(request, kurs_id, ders_id):
    """
    Bir dersin detayını (videoyu) gösterir.
    Sadece paket sahibi olan kullanıcılar erişebilir.
    """
    if not request.user.is_authenticated:
        return render(request, 'dersler/erisim_engellendi.html', {'sebep': 'giris_gerekli'})

    if not PaketSiparisi.objects.filter(user=request.user, odeme_tamamlandi=True).exists():
        return render(request, 'dersler/erisim_engellendi.html', {'sebep': 'paket_gerekli'})

    ders = get_object_or_404(Ders, kurs_id=kurs_id, pk=ders_id)
    return render(request, 'dersler/ders_detay.html', {'ders': ders})
