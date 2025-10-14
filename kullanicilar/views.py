# kullanicilar/views.py
from django.shortcuts import render, redirect
from .forms import KayitFormu
from .models import Profil
from django.contrib import messages
from django.utils import timezone


def kayit_view(request):
    if request.method == 'POST':
        form = KayitFormu(request.POST)
        if form.is_valid():
            user = form.save()
            telefon = form.cleaned_data.get('telefon')
            Profil.objects.create(user=user, telefon=telefon, onaylandi=True, kayit_tarihi=timezone.now())
            messages.success(request, 'Tebrikler başarıyla kaydoldunuz.')

            return redirect('login')
    else:
        form = KayitFormu()
    return render(request, 'registration/kayit.html', {'form': form})
