# odeme/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Kitap, Sepet, SepetUrunu, Siparis, SiparisUrunu
from .forms import SiparisForm
from kullanicilar.models import Profil
from decimal import Decimal
import uuid


# --- SEPET YARDIMCI FONKSİYONLARI ---

def _get_sepet(request):
    if request.user.is_authenticated:
        sepet, created = Sepet.objects.get_or_create(user=request.user)
    else:
        session_key = request.session.session_key
        if not session_key:
            request.session.create()
            session_key = request.session.session_key
        sepet, created = Sepet.objects.get_or_create(session_key=session_key, user__isnull=True)
    return sepet


# --- VIEW'LAR ---

def sepeti_goruntule(request):
    sepet = _get_sepet(request)
    return render(request, 'odeme/sepet.html', {'sepet': sepet})


def sepete_ekle(request, kitap_id):
    kitap = get_object_or_404(Kitap, id=kitap_id)
    sepet = _get_sepet(request)

    sepet_urunu, created = SepetUrunu.objects.get_or_create(sepet=sepet, kitap=kitap)
    if not created:
        sepet_urunu.adet += 1
        sepet_urunu.save()
        messages.success(request, f'"{kitap.baslik}" sepetinizdeki miktarı güncellendi.')
    else:
        messages.success(request, f'"{kitap.baslik}" sepetinize eklendi.')

    return redirect('odeme:sepeti_goruntule')


def sepetten_cikar(request, urun_id):
    sepet = _get_sepet(request)
    urun = get_object_or_404(SepetUrunu, id=urun_id, sepet=sepet)
    urun.delete()
    messages.info(request, 'Ürün sepetten çıkarıldı.')
    return redirect('odeme:sepeti_goruntule')


def sepet_adet_guncelle(request, urun_id, islem):
    sepet = _get_sepet(request)
    urun = get_object_or_404(SepetUrunu, id=urun_id, sepet=sepet)

    if islem == 'arttir':
        urun.adet += 1
        urun.save()
    elif islem == 'azalt':
        if urun.adet > 1:
            urun.adet -= 1
            urun.save()
        else:
            urun.delete()

    return redirect('odeme:sepeti_goruntule')


@login_required
def odeme_yap(request):
    sepet = _get_sepet(request)
    if not sepet.items.exists():
        messages.warning(request, 'Sepetiniz boş.')
        return redirect('odeme:kitap_listesi')

    if request.method == 'POST':
        form = SiparisForm(request.POST)
        if form.is_valid():
            # Sipariş Oluştur
            siparis = form.save(commit=False)
            siparis.user = request.user
            siparis.toplam_tutar = sepet.toplam_tutar
            siparis.save()

            # Sepet Ürünlerini Sipariş Ürünlerine Dönüştür
            for item in sepet.items.all():
                SiparisUrunu.objects.create(
                    siparis=siparis,
                    kitap=item.kitap,
                    fiyat=item.kitap.fiyat,
                    adet=item.adet
                )

            # Sepeti Temizle
            sepet.items.all().delete()

            messages.success(request, 'Siparişiniz başarıyla alındı!')
            return redirect('kullanicilar:hesabim')  # Siparişlerim sayfasına yönlendir
    else:
        initial_data = {
            'ad': request.user.first_name,
            'soyad': request.user.last_name,
            'email': request.user.email
        }
        # Eğer profilde telefon varsa onu da çekebiliriz
        try:
            if request.user.profil.telefon:
                initial_data['telefon'] = request.user.profil.telefon
        except:
            pass

        form = SiparisForm(initial=initial_data)

    context = {
        'form': form,
        'sepet': sepet
    }
    return render(request, 'odeme/odeme_sayfasi.html', context)


# --- MEVCUT KİTAP VIEW'LARI (Güncellendi) ---

def kitap_listesi(request):
    kitaplar = Kitap.objects.all()
    # İndirim mantığı istenirse buraya eklenebilir, şimdilik sade tutuyoruz
    return render(request, 'odeme/kitap_listesi.html', {'kitaplar': kitaplar})


def kitap_detay_view(request, kitap_id):
    kitap = get_object_or_404(Kitap, id=kitap_id)
    return render(request, 'odeme/kitap_detay.html', {'kitap': kitap})


# --- DİĞER ---
def satis_sozlesmesi(request):
    return render(request, 'odeme/satis_sozlesmesi.html')


def teslimat_iade_sartlari(request):
    return render(request, 'odeme/teslimat_iade.html')


def sinav_bilgilendirme(request):  # İsteğe bağlı kalabilir veya silinebilir
    return render(request, 'odeme/sinav_bilgilendirme.html')


def sinav_satin_al(request):  # Yönlendirme veya 404
    return redirect('anasayfa')


def kayit_basarili(request):
    return render(request, 'odeme/kayit_basarili.html')


def kayit_mevcut(request):
    return render(request, 'odeme/kayit_mevcut.html')
