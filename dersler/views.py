from django.shortcuts import render, get_object_or_404
from .models import Kurs, Ders
from django.contrib.auth.decorators import login_required # Bu satırı ekledik


def anasayfa_view(request):
    return render(request, 'anasayfa.html')

@login_required # Bu satırı ekledik
def kurs_listesi(request):
    kurslar = Kurs.objects.all()
    return render(request, 'dersler/kurs_listesi.html', {'kurslar': kurslar})

@login_required # Bu satırı ekledik
def kurs_detay(request, kurs_id):
    kurs = get_object_or_404(Kurs, pk=kurs_id)
    return render(request, 'dersler/kurs_detay.html', {'kurs': kurs})

@login_required # Bu satırı ekledik
def ders_detay(request, kurs_id, ders_id):
    ders = get_object_or_404(Ders, kurs_id=kurs_id, pk=ders_id)
    return render(request, 'dersler/ders_detay.html', {'ders': ders})