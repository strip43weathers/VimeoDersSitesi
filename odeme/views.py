# odeme/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Sinav, SinavSiparisi
from django.contrib import messages


def sinav_bilgilendirme(request):
    """Sınav hakkında bilgi veren ve ödeme sayfasına yönlendiren sayfa."""
    return render(request, 'odeme/sinav_bilgilendirme.html')


@login_required
def sinav_satin_al(request):
    # Kullanıcının daha önce bu sınavı alıp almadığını kontrol et
    mevcut_siparis = SinavSiparisi.objects.filter(user=request.user, odeme_tamamlandi=True).first()
    if mevcut_siparis:
        # Eğer siparişi varsa, onu "kayıt mevcut" sayfasına yönlendir
        return redirect('odeme:kayit_mevcut')

    sinav, created = Sinav.objects.get_or_create(id=1)

    if request.method == 'POST':
        payment_is_successful = True

        if payment_is_successful:
            SinavSiparisi.objects.create(user=request.user, sinav=sinav, odeme_tamamlandi=True)
            return redirect('odeme:kayit_basarili')
        else:
            messages.error(request, 'Ödeme sırasında bir hata oluştu.')
            return redirect('odeme:sinav_satin_al')

    return render(request, 'odeme/sinav_satin_al.html', {'sinav': sinav})


@login_required
def kayit_basarili(request):
    return render(request, 'odeme/kayit_basarili.html')


@login_required
def kayit_mevcut(request):
    return render(request, 'odeme/kayit_mevcut.html')


def satis_sozlesmesi(request):
    """Satış sözleşmesini gösteren sayfa."""
    return render(request, 'odeme/satis_sozlesmesi.html')
