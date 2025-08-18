# dosya: oyunlar/views.py
from django.shortcuts import render
from .models import Oyun
from django.contrib.auth.decorators import login_required # Bu import'u ekleyin

# Bu view artık SADECE herkese açık oyunları gösterecek
def oyun_listesi(request):
    oyunlar = Oyun.objects.filter(sadece_uyelere_ozel=False)
    context = {
        'oyunlar': oyunlar
    }
    return render(request, 'oyunlar/oyun_listesi.html', context)

# Üyelere özel oyunlar için YENİ VIEW
@login_required
def ozel_oyun_listesi(request):
    ozel_oyunlar = Oyun.objects.filter(sadece_uyelere_ozel=True)
    context = {
        'oyunlar': ozel_oyunlar
    }
    return render(request, 'oyunlar/ozel_oyun_listesi.html', context)
