from django.shortcuts import render
from .models import Oyun
from django.contrib.auth.decorators import login_required


def oyun_listesi(request):
    oyunlar = Oyun.objects.filter(sadece_uyelere_ozel=False)
    context = {
        'oyunlar': oyunlar
    }
    return render(request, 'oyunlar/oyun_listesi.html', context)


@login_required
def ozel_oyun_listesi(request):
    ozel_oyunlar = Oyun.objects.filter(sadece_uyelere_ozel=True)
    context = {
        'oyunlar': ozel_oyunlar
    }
    return render(request, 'oyunlar/ozel_oyun_listesi.html', context)
