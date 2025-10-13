# oyunlar/views.py

from django.shortcuts import render
from .models import Oyun
from odeme.models import PaketSiparisi  # PaketSiparisi modelini import ediyoruz


def oyun_listesi(request):
    """Herkesin görebileceği genel oyunları listeler."""
    oyunlar = Oyun.objects.filter(sadece_uyelere_ozel=False)

    # Kullanıcının paket sahibi olup olmadığını şablona göndermek için kontrol edelim
    kullanici_paket_sahibi_mi = False
    if request.user.is_authenticated:
        kullanici_paket_sahibi_mi = PaketSiparisi.objects.filter(user=request.user, odeme_tamamlandi=True).exists()

    context = {
        'oyunlar': oyunlar,
        'kullanici_paket_sahibi_mi': kullanici_paket_sahibi_mi
    }
    return render(request, 'oyunlar/oyun_listesi.html', context)


def ozel_oyun_listesi(request):
    """Sadece paket satın almış kullanıcıların görebileceği özel oyunları listeler."""

    # 1. Kullanıcı giriş yapmış mı? Yapmamışsa engelleme sayfasına yönlendir.
    if not request.user.is_authenticated:
        return render(request, 'dersler/erisim_engellendi.html', {'sebep': 'giris_gerekli'})

    # 2. Giriş yapmış ama paketi var mı? Yoksa engelleme sayfasına yönlendir.
    if not PaketSiparisi.objects.filter(user=request.user, odeme_tamamlandi=True).exists():
        return render(request, 'dersler/erisim_engellendi.html', {'sebep': 'paket_gerekli'})

    # Yetkisi varsa, özel oyunları listele
    ozel_oyunlar = Oyun.objects.filter(sadece_uyelere_ozel=True)
    context = {
        'oyunlar': ozel_oyunlar
    }
    return render(request, 'oyunlar/ozel_oyun_listesi.html', context)
