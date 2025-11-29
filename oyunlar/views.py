# oyunlar/views.py

from django.shortcuts import render
from .models import Oyun
from odeme.models import PaketSiparisi  # PaketSiparisi modelini import ediyoruz
from kullanicilar.models import Profil

def oyun_listesi(request):
    """Herkesin görebileceği genel oyunları listeler."""
    oyunlar = Oyun.objects.filter(sadece_uyelere_ozel=False)

    # Kullanıcının paket sahibi olup olmadığını şablona göndermek için kontrol edelim
    kullanici_paket_sahibi_mi = False
    ozel_erisim_var = False

    if request.user.is_authenticated:
        kullanici_paket_sahibi_mi = PaketSiparisi.objects.filter(user=request.user, odeme_tamamlandi=True).exists()

        # <-- ÖZEL ERİŞİM KONTROLÜ BAŞLANGICI -->
        try:
            ozel_erisim_var = request.user.profil.ozel_erisim
        except Profil.DoesNotExist:
            ozel_erisim_var = False
        # <-- ÖZEL ERİŞİM KONTROLÜ BİTİŞİ -->

    context = {
        'oyunlar': oyunlar,
        'kullanici_paket_sahibi_mi': kullanici_paket_sahibi_mi,
        'ozel_erisim_var': ozel_erisim_var,  # <-- Şablona gönderiyoruz
    }
    return render(request, 'oyunlar/oyun_listesi.html', context)


def ozel_oyun_listesi(request):
    """Sadece paket satın almış VEYA özel erişimi olan kullanıcıların görebileceği oyunlar."""

    # 1. Kullanıcı giriş yapmış mı?
    if not request.user.is_authenticated:
        return render(request, 'dersler/erisim_engellendi.html', {'sebep': 'giris_gerekli'})

    # 2. Giriş yapmış, paket veya özel erişim kontrolü
    paket_var = PaketSiparisi.objects.filter(user=request.user, odeme_tamamlandi=True).exists()

    ozel_erisim = False
    try:
        ozel_erisim = request.user.profil.ozel_erisim
    except Profil.DoesNotExist:
        pass

    # Hem paketi yoksa hem de özel erişimi yoksa engelle
    if not paket_var and not ozel_erisim:
        return render(request, 'dersler/erisim_engellendi.html', {'sebep': 'paket_gerekli'})

    # Yetkisi varsa listele
    ozel_oyunlar = Oyun.objects.filter(sadece_uyelere_ozel=True)
    context = {
        'oyunlar': ozel_oyunlar
    }
    return render(request, 'oyunlar/ozel_oyun_listesi.html', context)
