# dersler/views.py

from django.shortcuts import render, get_object_or_404
from .models import Kurs, Ders
from blog.models import BlogYazisi
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
    erisim_var = False

    if request.user.is_authenticated:
        # Profil modeli 'signals' ile otomatik oluşsa da garanti olsun diye hasattr ile kontrol ediyoruz.
        if hasattr(request.user, 'profil') and request.user.profil.erisim_izni_var_mi():
            erisim_var = True

    context = {
        'kurslar': kurslar,
        'erisim_var': erisim_var, # Template tarafında artık sadece bu değişkene bakılacak
    }
    return render(request, 'dersler/kurs_listesi.html', context)


def kurs_detay(request, kurs_id):
    if not request.user.is_authenticated:
        return render(request, 'dersler/erisim_engellendi.html', {'sebep': 'giris_gerekli'})

    # Tek merkezli erişim kontrolü
    erisim_var = False
    if hasattr(request.user, 'profil') and request.user.profil.erisim_izni_var_mi():
        erisim_var = True

    if not erisim_var:
        return render(request, 'dersler/erisim_engellendi.html', {'sebep': 'paket_gerekli'})

    kurs = get_object_or_404(Kurs, pk=kurs_id)
    return render(request, 'dersler/kurs_detay.html', {'kurs': kurs})


def ders_detay(request, kurs_id, ders_id):
    if not request.user.is_authenticated:
        return render(request, 'dersler/erisim_engellendi.html', {'sebep': 'giris_gerekli'})

    # Tek merkezli erişim kontrolü
    erisim_var = False
    if hasattr(request.user, 'profil') and request.user.profil.erisim_izni_var_mi():
        erisim_var = True

    if not erisim_var:
        return render(request, 'dersler/erisim_engellendi.html', {'sebep': 'paket_gerekli'})

    ders = get_object_or_404(Ders, kurs_id=kurs_id, pk=ders_id)
    return render(request, 'dersler/ders_detay.html', {'ders': ders})
