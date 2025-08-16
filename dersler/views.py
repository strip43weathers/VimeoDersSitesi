from django.shortcuts import render, get_object_or_404
from .models import Kurs, Ders
from django.contrib.auth.decorators import login_required
from django.db.models import Q  # Kompleks sorgular için import edildi
from django.http import HttpResponseForbidden  # Erişim engellendi hatası için import edildi


def anasayfa_view(request):
    return render(request, 'anasayfa.html')


@login_required
def kurs_listesi(request):
    # Kullanıcının görebileceği kursları filtrele:
    # 1. Herkese açık olanlar
    # 2. VEYA kullanıcının izinli olduğu kurslar
    kurslar = Kurs.objects.filter(
        Q(herkese_acik=True) | Q(izinli_kullanicilar=request.user)
    ).distinct()  # Aynı kursun iki kez gelmesini engellemek için
    return render(request, 'dersler/kurs_listesi.html', {'kurslar': kurslar})


@login_required
def kurs_detay(request, kurs_id):
    kurs = get_object_or_404(Kurs, pk=kurs_id)

    # Erişim Kontrolü:
    # Eğer kurs herkese açık değilse VE kullanıcı izinli listede değilse...
    if not kurs.herkese_acik and request.user not in kurs.izinli_kullanicilar.all():
        # ...erişimi engelle.
        return render(request, '403.html', status=403)

    return render(request, 'dersler/kurs_detay.html', {'kurs': kurs})


@login_required
def ders_detay(request, kurs_id, ders_id):
    kurs = get_object_or_404(Kurs, pk=kurs_id)

    # Erişim kontrolünü buraya da ekliyoruz
    if not kurs.herkese_acik and request.user not in kurs.izinli_kullanicilar.all():
        return render(request, '403.html', status=403)

    ders = get_object_or_404(Ders, kurs_id=kurs_id, pk=ders_id)
    return render(request, 'dersler/ders_detay.html', {'ders': ders})


# Diğer view fonksiyonlarınız (hakkimizda, sss vs.) aynı kalacak...
def hakkimizda_view(request):
    return render(request, 'hakkimizda.html')


def sss_view(request):
    return render(request, 'sss.html')


def gizlilik_view(request):
    return render(request, 'gizlilik.html')


def kullanim_view(request):
    return render(request, 'kullanim.html')
