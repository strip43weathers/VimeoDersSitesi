# odeme/views.py

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Sinav, SinavSiparisi
from django.contrib import messages
from .forms import SiparisForm


def sinav_bilgilendirme(request):
    """Sınav hakkında bilgi veren ve ödeme sayfasına yönlendiren sayfa."""
    return render(request, 'odeme/sinav_bilgilendirme.html')


@login_required
def sinav_satin_al(request):
    mevcut_siparis = SinavSiparisi.objects.filter(user=request.user, odeme_tamamlandi=True).first()
    if mevcut_siparis:
        return redirect('odeme:kayit_mevcut')

    sinav, created = Sinav.objects.get_or_create(id=1)

    if request.method == 'POST':
        form = SiparisForm(request.POST)
        if form.is_valid():
            # Ödeme işleminin başarılı olduğunu varsayıyoruz.
            # Gerçek bir ödeme entegrasyonunda bu kısım değişecektir.
            payment_is_successful = True

            if payment_is_successful:
                siparis = form.save(commit=False)
                siparis.user = request.user
                siparis.sinav = sinav
                siparis.odeme_tamamlandi = True
                siparis.save()
                return redirect('odeme:kayit_basarili')
            else:
                messages.error(request, 'Ödeme sırasında bir hata oluştu.')
    else:
        # GET request'i için boş bir form oluştur
        form = SiparisForm()

    return render(request, 'odeme/sinav_satin_al.html', {'sinav': sinav, 'form': form})


@login_required
def kayit_basarili(request):
    return render(request, 'odeme/kayit_basarili.html')


@login_required
def kayit_mevcut(request):
    return render(request, 'odeme/kayit_mevcut.html')


def satis_sozlesmesi(request):
    """Satış sözleşmesini gösteren sayfa."""
    return render(request, 'odeme/satis_sozlesmesi.html')
