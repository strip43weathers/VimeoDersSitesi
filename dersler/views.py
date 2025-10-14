# dersler/views.py

from django.shortcuts import render, get_object_or_404
from .models import Kurs, Ders
from odeme.models import PaketSiparisi
from blog.models import BlogYazisi
import datetime
from django.utils import timezone


def anasayfa_view(request):
    """
    Ana sayfayı render eder. Blog yazılarından son 3 tanesini de context'e ekler.
    """
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
    Sadece paket sahibi olan kullanıcılar veya eski kullanıcılar erişebilir.
    """
    if not request.user.is_authenticated:
        return render(request, 'dersler/erisim_engellendi.html', {'sebep': 'giris_gerekli'})

    # --- KONTROL MEKANİZMASI ---

    # 1. Kullanıcının ücretli bir paketi var mı diye kontrol et.
    paket_sahibi = PaketSiparisi.objects.filter(user=request.user, odeme_tamamlandi=True).exists()

    # 2. Eğer paketi yoksa, eski bir kullanıcı mı diye kontrol et.
    is_eski_kullanici = False
    if not paket_sahibi:
        # !!! DİKKAT: BU TARİHİ KENDİ SİSTEMİNİZİN GEÇİŞ TARİHİYLE DEĞİŞTİRİN !!!
        # Örneğin, sistem 13 Ekim 2025'te devreye girdiyse: datetime(2025, 10, 13)
        gecis_tarihi = timezone.make_aware(datetime.datetime(2025, 10, 15))

        # Kullanıcının asıl kayıt tarihine bakıyoruz.
        if request.user.date_joined < gecis_tarihi:
            is_eski_kullanici = True

    # 3. Eğer kullanıcı ne paket sahibi ne de eski kullanıcı ise, erişimi engelle.
    if not paket_sahibi and not is_eski_kullanici:
        return render(request, 'dersler/erisim_engellendi.html', {'sebep': 'paket_gerekli'})

    # Eğer buraya kadar geldiyse, kullanıcı yetkilidir.
    kurs = get_object_or_404(Kurs, pk=kurs_id)
    return render(request, 'dersler/kurs_detay.html', {'kurs': kurs})


def ders_detay(request, kurs_id, ders_id):
    """
    Bir dersin detayını (videoyu) gösterir.
    Sadece paket sahibi olan kullanıcılar veya eski kullanıcılar erişebilir.
    """
    if not request.user.is_authenticated:
        return render(request, 'dersler/erisim_engellendi.html', {'sebep': 'giris_gerekli'})

    # --- KONTROL MEKANİZMASI (Yukarıdakinin aynısı) ---
    paket_sahibi = PaketSiparisi.objects.filter(user=request.user, odeme_tamamlandi=True).exists()

    is_eski_kullanici = False
    if not paket_sahibi:
        # !!! DİKKAT: BU TARİHİ KENDİ SİSTEMİNİZİN GEÇİŞ TARİHİYLE DEĞİŞTİRİN !!!
        gecis_tarihi = timezone.make_aware(datetime.datetime(2025, 10, 15))
        if request.user.date_joined < gecis_tarihi:
            is_eski_kullanici = True

    if not paket_sahibi and not is_eski_kullanici:
        return render(request, 'dersler/erisim_engellendi.html', {'sebep': 'paket_gerekli'})

    # Kullanıcı yetkiliyse ders detayını göster.
    ders = get_object_or_404(Ders, kurs_id=kurs_id, pk=ders_id)
    return render(request, 'dersler/ders_detay.html', {'ders': ders})
