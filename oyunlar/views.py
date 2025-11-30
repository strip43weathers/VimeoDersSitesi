# oyunlar/views.py

from django.shortcuts import render
from .models import Oyun
# from odeme.models import PaketSiparisi  <-- BU SATIR ARTIK YOK, IMPORTU KALDIRDIK
from kullanicilar.models import Profil

def oyun_listesi(request):
    """Herkesin görebileceği genel oyunları listeler."""
    oyunlar = Oyun.objects.filter(sadece_uyelere_ozel=False)

    # Paket sistemi değiştiği için şimdilik false kabul ediyoruz
    kullanici_paket_sahibi_mi = False
    ozel_erisim_var = False

    if request.user.is_authenticated:
        # Sadece özel erişimi kontrol ediyoruz
        try:
            ozel_erisim_var = request.user.profil.ozel_erisim
        except Profil.DoesNotExist:
            ozel_erisim_var = False

    context = {
        'oyunlar': oyunlar,
        'kullanici_paket_sahibi_mi': kullanici_paket_sahibi_mi,
        'ozel_erisim_var': ozel_erisim_var,
    }
    return render(request, 'oyunlar/oyun_listesi.html', context)


def ozel_oyun_listesi(request):
    """Sadece özel erişimi olan kullanıcıların görebileceği oyunlar."""

    if not request.user.is_authenticated:
        return render(request, 'dersler/erisim_engellendi.html', {'sebep': 'giris_gerekli'})

    ozel_erisim = False
    try:
        ozel_erisim = request.user.profil.ozel_erisim
    except Profil.DoesNotExist:
        pass

    # Paket kontrolü yerine sadece özel erişim kontrolü yapıyoruz
    if not ozel_erisim:
        return render(request, 'dersler/erisim_engellendi.html', {'sebep': 'paket_gerekli'})

    ozel_oyunlar = Oyun.objects.filter(sadece_uyelere_ozel=True)
    context = {
        'oyunlar': ozel_oyunlar
    }
    return render(request, 'oyunlar/ozel_oyun_listesi.html', context)
