# dersler/views.py

from django.shortcuts import render, get_object_or_404
from .models import Kurs, Ders
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponseForbidden
from sayfalar.models import RehberVideo


def anasayfa_view(request):
    # Sadece ana sayfa için aktif olan videoyu çek
    rehber_video = RehberVideo.objects.filter(aktif=True, sayfa='anasayfa').first()
    context = {
        'rehber_video': rehber_video
    }
    return render(request, 'anasayfa.html', context)


@login_required
def kurs_listesi(request):
    # Orijinal hali: Herkese açık veya özel izinli kursları listeler
    kurslar = Kurs.objects.filter(
        Q(herkese_acik=True) | Q(izinli_kullanicilar=request.user)
    ).distinct()
    return render(request, 'dersler/kurs_listesi.html', {'kurslar': kurslar})


@login_required
def kurs_detay(request, kurs_id):
    kurs = get_object_or_404(Kurs, pk=kurs_id)

    # Orijinal hali: Herkese açık değilse ve kullanıcı izinli değilse engelle
    if not kurs.herkese_acik and request.user not in kurs.izinli_kullanicilar.all():
        return render(request, '403.html', status=403)

    return render(request, 'dersler/kurs_detay.html', {'kurs': kurs})


@login_required
def ders_detay(request, kurs_id, ders_id):
    kurs = get_object_or_404(Kurs, pk=kurs_id)

    # Orijinal hali: Herkese açık değilse ve kullanıcı izinli değilse engelle
    if not kurs.herkese_acik and request.user not in kurs.izinli_kullanicilar.all():
        return render(request, '403.html', status=403)

    ders = get_object_or_404(Ders, kurs_id=kurs_id, pk=ders_id)
    return render(request, 'dersler/ders_detay.html', {'ders': ders})
