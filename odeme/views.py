# odeme/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Sinav, SinavSiparisi, EgitimPaketi, PaketSiparisi
from django.contrib import messages
from .forms import SiparisForm, PaketSiparisForm
from django.utils import timezone
import datetime
from kullanicilar.models import Profil
from decimal import Decimal

# --- MEVCUT SINAV VIEW'LARI ---

def sinav_bilgilendirme(request):
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
            payment_is_successful = True
            if payment_is_successful:
                siparis = form.save(commit=False)
                siparis.user = request.user
                siparis.sinav = sinav
                siparis.odeme_tamamlandi = True
                siparis.save()
                return redirect('odeme:kayit_basarili') # Sınav için doğru yönlendirme
            else:
                messages.error(request, 'Ödeme sırasında bir hata oluştu.')
                return redirect('odeme:sinav_satin_al')
    else:
        form = SiparisForm()
    return render(request, 'odeme/sinav_satin_al.html', {'sinav': sinav, 'form': form})

@login_required
def kayit_basarili(request):
    return render(request, 'odeme/kayit_basarili.html')

@login_required
def kayit_mevcut(request):
    return render(request, 'odeme/kayit_mevcut.html')

def satis_sozlesmesi(request):
    return render(request, 'odeme/satis_sozlesmesi.html')


# --- YENİ EĞİTİM PAKETİ VIEW'LARI ---

def paket_listesi(request):
    paketler = EgitimPaketi.objects.all()
    indirim_aktif = False
    indirim_bitis_tarihi = None  # Bitiş tarihini tutmak için değişken

    if request.user.is_authenticated:
        try:
            profil = Profil.objects.get(user=request.user)
            kayit_suresi = timezone.now() - profil.kayit_tarihi

            # Kayıt süresi 1 günden az ise indirim aktiftir
            if kayit_suresi < datetime.timedelta(days=1):
                indirim_aktif = True
                # Bitiş tarihini hesapla: Kayıt tarihi + 1 gün
                indirim_bitis_tarihi = profil.kayit_tarihi + datetime.timedelta(days=1)
                for paket in paketler:
                    paket.indirimli_fiyat = (paket.fiyat * Decimal('0.90')).quantize(Decimal("0.01"))
        except Profil.DoesNotExist:
            pass

    context = {
        'paketler': paketler,
        'indirim_aktif': indirim_aktif,
        # Bitiş tarihini JavaScript'in anlayacağı bir formatta gönderiyoruz (ISO 8601)
        'indirim_bitis_tarihi': indirim_bitis_tarihi.isoformat() if indirim_bitis_tarihi else None
    }
    return render(request, 'odeme/paket_listesi.html', context)


@login_required
def paket_satin_al(request, paket_id):
    paket = get_object_or_404(EgitimPaketi, id=paket_id)
    mevcut_siparis = PaketSiparisi.objects.filter(user=request.user, paket=paket, odeme_tamamlandi=True).first()
    if mevcut_siparis:
        messages.info(request, f'"{paket.baslik}" paketine zaten sahipsiniz.')
        return redirect('odeme:paket_kayit_mevcut') # <-- PAKET İÇİN YENİ YÖNLENDİRME

    indirimli_fiyat = None
    try:
        profil = Profil.objects.get(user=request.user)
        if timezone.now() - profil.kayit_tarihi < datetime.timedelta(days=1):
            indirimli_fiyat = (paket.fiyat * Decimal('0.90')).quantize(Decimal("0.01"))
    except Profil.DoesNotExist:
        pass

    if request.method == 'POST':
        form = PaketSiparisForm(request.POST)
        if form.is_valid():
            payment_is_successful = True  # Ödeme mantığınızı buraya entegre edin
            if payment_is_successful:
                siparis = form.save(commit=False)
                siparis.user = request.user
                siparis.paket = paket
                siparis.odeme_tamamlandi = True
                # İleride, sipariş anındaki fiyatı da sipariş modeline kaydedebilirsiniz.
                # siparis.fiyat = indirimli_fiyat if indirimli_fiyat is not None else paket.fiyat
                siparis.save()
                return redirect('odeme:paket_kayit_basarili') # <-- PAKET İÇİN YENİ YÖNLENDİRME
            else:
                messages.error(request, 'Ödeme sırasında bir hata oluştu.')
    else:
        form = PaketSiparisForm()

    context = {
        'paket': paket,
        'form': form,
        'indirimli_fiyat': indirimli_fiyat
    }
    return render(request, 'odeme/paket_satin_al.html', context)


# --- PAKETLER İÇİN YENİ EKLENEN VIEW'LAR ---
@login_required
def paket_kayit_basarili(request):
    return render(request, 'odeme/paket_kayit_basarili.html')

@login_required
def paket_kayit_mevcut(request):
    return render(request, 'odeme/paket_kayit_mevcut.html')
