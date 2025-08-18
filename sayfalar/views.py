# dosya: sayfalar/views.py
from django.shortcuts import render, get_object_or_404
from .models import Sayfa

def sayfa_detay(request, slug):
    sayfa = get_object_or_404(Sayfa, slug=slug)
    context = {
        'sayfa': sayfa
    }
    return render(request, 'sayfalar/sayfa_detay.html', context)