# kullanicilar/views.py
from django.shortcuts import render, redirect
from .forms import KayitFormu
from .models import Profil
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from odeme.models import Siparis


def kayit_view(request):
    if request.method == 'POST':
        form = KayitFormu(request.POST)
        if form.is_valid():
            user = form.save()
            # Kullanıcı kaydedildiği anda signals.py devreye girer ve boş bir Profil oluşturur.

            # Formdan gelen telefon bilgisini alıp profile ekleyelim:
            telefon = form.cleaned_data.get('telefon')

            # Profil nesnesine erişip güncelliyoruz
            if hasattr(user, 'profil'):
                user.profil.telefon = telefon
                user.profil.onaylandi = True  # Kayıt olan kullanıcıları otomatik onaylı sayıyoruz
                user.profil.save()

            messages.success(request, 'Tebrikler başarıyla kaydoldunuz.')
            return redirect('login')
    else:
        form = KayitFormu()
    return render(request, 'registration/kayit.html', {'form': form})


@login_required
def hesabim_view(request):
    siparisler = Siparis.objects.filter(user=request.user).order_by('-tarih')
    return render(request, 'kullanicilar/hesabim.html', {'siparisler': siparisler})
