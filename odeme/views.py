# odeme/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Kitap, Sepet, SepetUrunu, Siparis, SiparisUrunu
from .forms import SiparisForm
from kullanicilar.models import Profil
from decimal import Decimal
import uuid
from django.utils import timezone
from datetime import timedelta


# --- YARDIMCI FONKSİYONLAR ---

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


def get_indirim_durumu(user):
    """
    Kullanıcı varsa ve kayıt tarihinden itibaren 24 saat geçmemişse
    indirim aktif döner.
    """
    if not user.is_authenticated:
        return False, None

    try:
        # Profil modelinizde kayit_tarihi olduğunu varsayıyoruz
        kayit_tarihi = user.profil.kayit_tarihi
        simdi = timezone.now()
        bitis_tarihi = kayit_tarihi + timedelta(hours=24)

        if simdi < bitis_tarihi:
            # ISO formatında string olarak döndürüyoruz (JS için)
            return True, bitis_tarihi.isoformat()
    except Exception as e:
        pass

    return False, None


# --- SEPET İŞLEMLERİ ---

def sepeti_goruntule(request):
    sepet = _get_sepet(request)

    # İndirim Kontrolü
    indirim_aktif, indirim_bitis = get_indirim_durumu(request.user)

    # Sepet toplamını hesapla
    toplam_tutar = sepet.toplam_tutar

    # Eğer indirim aktifse ve sepet boş değilse tutarı güncelle
    if indirim_aktif and toplam_tutar > 0:
        toplam_tutar = round(toplam_tutar * Decimal('0.90'), 2)

    # Sepet objesine geçici olarak indirimli tutarı atıyoruz (DB'ye kaydetmeden, sadece gösterim için)
    sepet.gosterilecek_tutar = toplam_tutar

    context = {
        'sepet': sepet,
        'indirim_aktif': indirim_aktif,
        'indirim_bitis_tarihi': indirim_bitis
    }
    return render(request, 'odeme/sepet.html', context)


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


# --- ÖDEME VE SİPARİŞ ---

@login_required
def odeme_yap(request):
    sepet = _get_sepet(request)
    if not sepet.items.exists():
        messages.warning(request, 'Sepetiniz boş.')
        return redirect('odeme:kitap_listesi')

    # İndirim Kontrolü
    indirim_aktif, indirim_bitis = get_indirim_durumu(request.user)

    # Ödenecek tutarı belirle
    odenecek_tutar = sepet.toplam_tutar
    if indirim_aktif:
        odenecek_tutar = round(odenecek_tutar * Decimal('0.90'), 2)

    # Sepet objesine template'de göstermek için atama yapıyoruz
    sepet.gosterilecek_tutar = odenecek_tutar

    if request.method == 'POST':
        form = SiparisForm(request.POST)
        if form.is_valid():
            # Sipariş Oluştur
            siparis = form.save(commit=False)
            siparis.user = request.user
            # İndirimli tutarı kaydediyoruz!
            siparis.toplam_tutar = odenecek_tutar
            siparis.save()

            # Sepet Ürünlerini Sipariş Ürünlerine Dönüştür
            for item in sepet.items.all():
                # Ürün bazlı fiyatı da indirimli kaydediyoruz
                satis_fiyati = item.kitap.fiyat
                if indirim_aktif:
                    satis_fiyati = round(satis_fiyati * Decimal('0.90'), 2)

                SiparisUrunu.objects.create(
                    siparis=siparis,
                    kitap=item.kitap,
                    fiyat=satis_fiyati,
                    adet=item.adet
                )

            # Sepeti Temizle
            sepet.items.all().delete()

            messages.success(request, 'Siparişiniz başarıyla alındı!')
            return redirect('kullanicilar:hesabim')
    else:
        initial_data = {
            'ad': request.user.first_name,
            'soyad': request.user.last_name,
            'email': request.user.email
        }
        try:
            if hasattr(request.user, 'profil') and request.user.profil.telefon:
                initial_data['telefon'] = request.user.profil.telefon
        except:
            pass

        form = SiparisForm(initial=initial_data)

    context = {
        'form': form,
        'sepet': sepet,
        'indirim_aktif': indirim_aktif,
        'indirim_bitis_tarihi': indirim_bitis
    }
    return render(request, 'odeme/odeme_sayfasi.html', context)


# --- KİTAP GÖRÜNTÜLEME ---

def kitap_listesi(request):
    kitaplar = Kitap.objects.all()

    # İndirim Kontrolü
    indirim_aktif, indirim_bitis = get_indirim_durumu(request.user)

    if indirim_aktif:
        for kitap in kitaplar:
            # %10 İndirim uygula (Geçici attribute)
            kitap.indirimli_fiyat = round(kitap.fiyat * Decimal('0.90'), 2)

    context = {
        'kitaplar': kitaplar,
        'indirim_aktif': indirim_aktif,
        'indirim_bitis_tarihi': indirim_bitis
    }
    return render(request, 'odeme/kitap_listesi.html', context)


def kitap_detay_view(request, kitap_id):
    kitap = get_object_or_404(Kitap, id=kitap_id)

    # İndirim Kontrolü
    indirim_aktif, indirim_bitis = get_indirim_durumu(request.user)
    indirimli_fiyat = None

    if indirim_aktif:
        indirimli_fiyat = round(kitap.fiyat * Decimal('0.90'), 2)

    context = {
        'kitap': kitap,
        'indirim_aktif': indirim_aktif,
        'indirim_bitis_tarihi': indirim_bitis,
        'indirimli_fiyat': indirimli_fiyat
    }
    return render(request, 'odeme/kitap_detay.html', context)


# --- STATİK SAYFALAR ---

def satis_sozlesmesi(request):
    return render(request, 'odeme/satis_sozlesmesi.html')


def teslimat_iade_sartlari(request):
    return render(request, 'odeme/teslimat_iade.html')
