# dersler/views.py

from django.shortcuts import render, get_object_or_404
from .models import Kurs, Ders
from odeme.models import PaketSiparisi
from blog.models import BlogYazisi
import datetime
from django.utils import timezone
from sayfalar.models import RehberVideo
from kullanicilar.models import Profil # <--- BU SATIRI EKLEYİN


def anasayfa_view(request):
    """
    Ana sayfayı render eder. Blog yazılarından son 3 tanesini ve
    ana sayfa için aktif olan rehber videosunu context'e ekler.
    """
    recent_posts = BlogYazisi.objects.order_by('-olusturulma_tarihi')[:3]

    # Ana sayfa için aktif olan ilk rehber videoyu bul
    rehber_video = RehberVideo.objects.filter(sayfa='anasayfa', aktif=True).first()

    context = {
        'recent_posts': recent_posts,
        'rehber_video': rehber_video,  # Videoyu context'e ekle
    }

    return render(request, 'anasayfa.html', context)


def kurs_listesi(request):
    """
    Tüm kursları listeler ve kullanıcının eski veya paket sahibi olup olmadığını kontrol eder.
    """
    kurslar = Kurs.objects.all()
    kullanici_paket_sahibi_mi = False
    is_eski_kullanici = False  # Yeni kontrol değişkeni

    if request.user.is_authenticated:
        # Kullanıcının zaten bir paketi var mı diye kontrol et
        kullanici_paket_sahibi_mi = PaketSiparisi.objects.filter(user=request.user, odeme_tamamlandi=True).exists()

        # Eğer paketi yoksa, eski kullanıcı mı diye kontrol et
        if not kullanici_paket_sahibi_mi:
            # !!! ÖNEMLİ: Bu tarihi bir önceki adımda kullandığınız tarih ile aynı yapın !!!
            gecis_tarihi = timezone.make_aware(datetime.datetime(2025, 10, 25))

            if request.user.date_joined < gecis_tarihi:
                is_eski_kullanici = True

    context = {
        'kurslar': kurslar,
        'kullanici_paket_sahibi_mi': kullanici_paket_sahibi_mi,
        'is_eski_kullanici': is_eski_kullanici,  # Bu bilgiyi şablona gönderiyoruz
    }
    return render(request, 'dersler/kurs_listesi.html', context)


def kurs_detay(request, kurs_id):
    """
    Bir kursun detaylarını ve derslerini gösterir.
    Sadece paket sahibi olan kullanıcılar, eski kullanıcılar veya özel erişimi olanlar erişebilir.
    """
    if not request.user.is_authenticated:
        return render(request, 'dersler/erisim_engellendi.html', {'sebep': 'giris_gerekli'})

    # --- KONTROL MEKANİZMASI ---
    paket_sahibi = PaketSiparisi.objects.filter(user=request.user, odeme_tamamlandi=True).exists()

    is_eski_kullanici = False
    ozel_erisim = False
    try:
        ozel_erisim = request.user.profil.ozel_erisim
    except Profil.DoesNotExist:
        pass

    if not paket_sahibi and not ozel_erisim:
        # !!! DİKKAT: BU TARİHİ KENDİ SİSTEMİNİZİN GEÇİŞ TARİHİYLE DEĞİŞTİRİN !!!
        gecis_tarihi = timezone.make_aware(datetime.datetime(2025, 10, 25))

        if request.user.date_joined < gecis_tarihi:
            is_eski_kullanici = True

    if not paket_sahibi and not is_eski_kullanici and not ozel_erisim:
        return render(request, 'dersler/erisim_engellendi.html', {'sebep': 'paket_gerekli'})

    kurs = get_object_or_404(Kurs, pk=kurs_id)
    return render(request, 'dersler/kurs_detay.html', {'kurs': kurs})


def ders_detay(request, kurs_id, ders_id):
    """
    Bir dersin detayını (videoyu) gösterir.
    Sadece paket sahibi olan kullanıcılar, eski kullanıcılar veya özel erişimi olanlar erişebilir.
    """
    if not request.user.is_authenticated:
        return render(request, 'dersler/erisim_engellendi.html', {'sebep': 'giris_gerekli'})

    # --- KONTROL MEKANİZMASI (Yukarıdakinin aynısı) ---
    paket_sahibi = PaketSiparisi.objects.filter(user=request.user, odeme_tamamlandi=True).exists()

    is_eski_kullanici = False
    ozel_erisim = False
    try:
        ozel_erisim = request.user.profil.ozel_erisim
    except Profil.DoesNotExist:
        pass

    if not paket_sahibi and not ozel_erisim:
        # !!! DİKKAT: BU TARİHİ KENDİ SİSTEMİNİZİN GEÇİŞ TARİHİYLE DEĞİŞTİRİN !!!
        gecis_tarihi = timezone.make_aware(datetime.datetime(2025, 10, 25))
        if request.user.date_joined < gecis_tarihi:
            is_eski_kullanici = True

    if not paket_sahibi and not is_eski_kullanici and not ozel_erisim:
        return render(request, 'dersler/erisim_engellendi.html', {'sebep': 'paket_gerekli'})

    ders = get_object_or_404(Ders, kurs_id=kurs_id, pk=ders_id)
    return render(request, 'dersler/ders_detay.html', {'ders': ders})
