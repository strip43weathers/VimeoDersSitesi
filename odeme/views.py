# odeme/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib import messages
from .models import Kitap, Sepet, SepetUrunu, Siparis, SiparisUrunu, IndirimKodu
from .forms import SiparisForm, IndirimKoduForm
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
    if not user.is_authenticated:
        return False, None
    try:
        kayit_tarihi = user.profil.kayit_tarihi
        simdi = timezone.now()
        bitis_tarihi = kayit_tarihi + timedelta(hours=24)
        if simdi < bitis_tarihi:
            return True, bitis_tarihi.isoformat()
    except Exception as e:
        pass
    return False, None


# --- KUPON İŞLEMLERİ ---

@require_POST
def kupon_uygula(request):
    sepet = _get_sepet(request)
    form = IndirimKoduForm(request.POST)

    if form.is_valid():
        kod = form.cleaned_data['kod']
        try:
            kupon = IndirimKodu.objects.get(kod=kod, aktif=True)
            if kupon.gecerli_mi:
                sepet.uygulanan_kupon = kupon
                sepet.save()
                messages.success(request, f"%{kupon.indirim_orani} indirim uygulandı!")
            else:
                messages.error(request, "Bu kuponun süresi dolmuş veya kullanım limiti dolmuş.")
        except IndirimKodu.DoesNotExist:
            messages.error(request, "Geçersiz kupon kodu.")
            sepet.uygulanan_kupon = None
            sepet.save()

    return redirect('odeme:sepeti_goruntule')


def kupon_kaldir(request):
    sepet = _get_sepet(request)
    sepet.uygulanan_kupon = None
    sepet.save()
    messages.info(request, "Kupon kaldırıldı.")
    return redirect('odeme:sepeti_goruntule')


# --- SEPET İŞLEMLERİ ---

def sepeti_goruntule(request):
    sepet = _get_sepet(request)

    # Sepetteki kupon artık geçersizse (örn: başkası son kullanma hakkını kullandıysa) kaldır
    if sepet.uygulanan_kupon and not sepet.uygulanan_kupon.gecerli_mi:
        messages.warning(request, f"Sepetinizdeki '{sepet.uygulanan_kupon.kod}' kuponunun süresi veya limiti doldu.")
        sepet.uygulanan_kupon = None
        sepet.save()

    kupon_form = IndirimKoduForm()
    indirim_aktif, indirim_bitis = get_indirim_durumu(request.user)

    hesaplanan_tutar = sepet.sepet_son_tutar
    if indirim_aktif and hesaplanan_tutar > 0:
        hesaplanan_tutar = round(hesaplanan_tutar * Decimal('0.90'), 2)

    sepet.gosterilecek_tutar = hesaplanan_tutar

    context = {
        'sepet': sepet,
        'kupon_form': kupon_form,
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
        messages.success(request, f'"{kitap.baslik}" miktarı güncellendi.')
    else:
        messages.success(request, f'"{kitap.baslik}" sepete eklendi.')
    return redirect('odeme:sepeti_goruntule')


def sepetten_cikar(request, urun_id):
    sepet = _get_sepet(request)
    urun = get_object_or_404(SepetUrunu, id=urun_id, sepet=sepet)
    urun.delete()
    messages.info(request, 'Ürün çıkarıldı.')
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

    # Son kontrol: Kupon hala geçerli mi?
    if sepet.uygulanan_kupon and not sepet.uygulanan_kupon.gecerli_mi:
        messages.error(request, "Uygulanan kuponun limiti doldu veya süresi geçti.")
        sepet.uygulanan_kupon = None
        sepet.save()
        return redirect('odeme:sepeti_goruntule')

    indirim_aktif, indirim_bitis = get_indirim_durumu(request.user)
    odenecek_tutar = sepet.sepet_son_tutar
    if indirim_aktif and odenecek_tutar > 0:
        odenecek_tutar = round(odenecek_tutar * Decimal('0.90'), 2)

    sepet.gosterilecek_tutar = odenecek_tutar

    if request.method == 'POST':
        form = SiparisForm(request.POST)
        if form.is_valid():
            siparis = form.save(commit=False)
            siparis.user = request.user
            siparis.toplam_tutar = odenecek_tutar

            # Kupon İşlemleri
            if sepet.uygulanan_kupon:
                siparis.kullanilan_kupon = sepet.uygulanan_kupon.kod
                # Kullanım sayısını 1 artırıyoruz!
                sepet.uygulanan_kupon.kullanim_sayisi += 1
                sepet.uygulanan_kupon.save()

            siparis.save()

            for item in sepet.items.all():
                satis_fiyati = item.kitap.fiyat
                if indirim_aktif:  # Ürün bazlı indirim gösterimi için (opsiyonel)
                    satis_fiyati = round(satis_fiyati * Decimal('0.90'), 2)

                SiparisUrunu.objects.create(
                    siparis=siparis,
                    kitap=item.kitap,
                    fiyat=satis_fiyati,
                    adet=item.adet
                )

            sepet.uygulanan_kupon = None
            sepet.save()
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
    siralama = request.GET.get('sirala')
    kitaplar = Kitap.objects.all()

    if siralama == 'fiyat_artan':
        kitaplar = kitaplar.order_by('fiyat')
    elif siralama == 'fiyat_azalan':
        kitaplar = kitaplar.order_by('-fiyat')
    elif siralama == 'isim_a_z':
        kitaplar = kitaplar.order_by('baslik')
    elif siralama == 'isim_z_a':
        kitaplar = kitaplar.order_by('-baslik')
    elif siralama == 'yeni':
        kitaplar = kitaplar.order_by('-id')
    else:
        kitaplar = kitaplar.order_by('id')

    indirim_aktif, indirim_bitis = get_indirim_durumu(request.user)
    if indirim_aktif:
        for kitap in kitaplar:
            kitap.indirimli_fiyat = round(kitap.fiyat * Decimal('0.90'), 2)

    context = {
        'kitaplar': kitaplar,
        'indirim_aktif': indirim_aktif,
        'indirim_bitis_tarihi': indirim_bitis,
        'secili_siralama': siralama
    }
    return render(request, 'odeme/kitap_listesi.html', context)


def kitap_detay_view(request, kitap_id):
    kitap = get_object_or_404(Kitap, id=kitap_id)
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
