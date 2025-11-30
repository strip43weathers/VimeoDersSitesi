# dersler/views.py

from django.shortcuts import render, get_object_or_404
from .models import Kurs, Ders
# from odeme.models import PaketSiparisi  <-- BU SATIRI SİLİN VEYA YORUMA ALIN
from blog.models import BlogYazisi
import datetime
from django.utils import timezone
from sayfalar.models import RehberVideo
from kullanicilar.models import Profil


def anasayfa_view(request):
    recent_posts = BlogYazisi.objects.order_by('-olusturulma_tarihi')[:3]
    rehber_video = RehberVideo.objects.filter(sayfa='anasayfa', aktif=True).first()
    context = {
        'recent_posts': recent_posts,
        'rehber_video': rehber_video,
    }
    return render(request, 'anasayfa.html', context)


def kurs_listesi(request):
    kurslar = Kurs.objects.all()
    kullanici_paket_sahibi_mi = False  # Artık paket siparişi olmadığı için False
    is_eski_kullanici = False
    ozel_erisim_var = False

    if request.user.is_authenticated:
        try:
            ozel_erisim_var = request.user.profil.ozel_erisim
        except Profil.DoesNotExist:
            ozel_erisim_var = False

        # Paket kontrolünü kaldırdık, sadece eski kullanıcı ve özel erişime bakıyoruz
        if not ozel_erisim_var:
            gecis_tarihi = timezone.make_aware(datetime.datetime(2025, 10, 25))
            if request.user.date_joined < gecis_tarihi:
                is_eski_kullanici = True

    context = {
        'kurslar': kurslar,
        'kullanici_paket_sahibi_mi': kullanici_paket_sahibi_mi,
        'is_eski_kullanici': is_eski_kullanici,
        'ozel_erisim_var': ozel_erisim_var,
    }
    return render(request, 'dersler/kurs_listesi.html', context)


def kurs_detay(request, kurs_id):
    # ... (Erişim kontrollerini yukarıdaki mantığa göre basitleştirin) ...
    # Paket kontrolü satırlarını kaldırın ve is_eski_kullanici / ozel_erisim ile devam edin.
    if not request.user.is_authenticated:
        return render(request, 'dersler/erisim_engellendi.html', {'sebep': 'giris_gerekli'})

    is_eski_kullanici = False
    ozel_erisim = False
    try:
        ozel_erisim = request.user.profil.ozel_erisim
    except Profil.DoesNotExist:
        pass

    gecis_tarihi = timezone.make_aware(datetime.datetime(2025, 10, 25))
    if request.user.date_joined < gecis_tarihi:
        is_eski_kullanici = True

    if not is_eski_kullanici and not ozel_erisim:
        return render(request, 'dersler/erisim_engellendi.html',
                      {'sebep': 'paket_gerekli'})  # Mesajı genel tutabilirsiniz

    kurs = get_object_or_404(Kurs, pk=kurs_id)
    return render(request, 'dersler/kurs_detay.html', {'kurs': kurs})


def ders_detay(request, kurs_id, ders_id):
    # kurs_detay ile aynı mantıkta güncelleyin
    if not request.user.is_authenticated:
        return render(request, 'dersler/erisim_engellendi.html', {'sebep': 'giris_gerekli'})

    is_eski_kullanici = False
    ozel_erisim = False
    try:
        ozel_erisim = request.user.profil.ozel_erisim
    except Profil.DoesNotExist:
        pass

    gecis_tarihi = timezone.make_aware(datetime.datetime(2025, 10, 25))
    if request.user.date_joined < gecis_tarihi:
        is_eski_kullanici = True

    if not is_eski_kullanici and not ozel_erisim:
        return render(request, 'dersler/erisim_engellendi.html', {'sebep': 'paket_gerekli'})

    ders = get_object_or_404(Ders, kurs_id=kurs_id, pk=ders_id)
    return render(request, 'dersler/ders_detay.html', {'ders': ders})
