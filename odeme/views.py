# odeme/views.py

import iyzipay
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404, HttpResponse, reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
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

def get_client_ip(request):
    """Kullanıcının IP adresini alır (İyzico için gerekli)"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


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


# --- ÖDEME VE SİPARİŞ (REVİZE EDİLDİ) ---

@login_required
def odeme_yap(request):
    """
    Bu view artık sadece adres bilgilerini alır ve 'Sipariş' objesini oluşturur.
    Ödeme almak yerine, kullanıcıyı İyzico formunun olduğu 'odeme_baslat' view'ına yönlendirir.
    """
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
            siparis.odeme_tamamlandi = False  # Varsayılan olarak ödenmedi

            # Kupon İşlemleri
            if sepet.uygulanan_kupon:
                siparis.kullanilan_kupon = sepet.uygulanan_kupon.kod
                # Kullanım sayısını BURADA ARTIRMIYORUZ. Ödeme başarılı olunca artıracağız.

            siparis.save()

            # Sipariş ürünlerini oluştur
            for item in sepet.items.all():
                satis_fiyati = item.kitap.fiyat
                if indirim_aktif:
                    satis_fiyati = round(satis_fiyati * Decimal('0.90'), 2)

                SiparisUrunu.objects.create(
                    siparis=siparis,
                    kitap=item.kitap,
                    fiyat=satis_fiyati,
                    adet=item.adet
                )

            # NOT: Sepeti burada BOŞALTMADIK. Ödeme başarılı olursa boşaltacağız.

            # İyzico ödeme ekranına yönlendir
            return redirect('odeme:odeme_baslat', siparis_id=siparis.id)

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


@login_required
def odeme_baslat(request, siparis_id):
    """
    Oluşturulan sipariş için İyzico formu hazırlar ve ekrana basar.
    """
    siparis = get_object_or_404(Siparis, id=siparis_id, user=request.user)

    if siparis.odeme_tamamlandi:
        return redirect('kullanicilar:hesabim')

    # İyzico Seçenekleri
    options = {
        'api_key': settings.IYZICO_API_KEY,
        'secret_key': settings.IYZICO_SECRET_KEY,
        'base_url': settings.IYZICO_BASE_URL
    }

    # Callback URL (Localhost veya Render için dinamik)
    callback_url = request.build_absolute_uri(reverse('odeme:odeme_sonuc'))

    request_iyzico = {
        'locale': 'tr',
        'conversationId': str(siparis.id),
        'price': str(siparis.toplam_tutar),
        'paidPrice': str(siparis.toplam_tutar),
        'currency': 'TRY',
        'basketId': str(siparis.id),
        'paymentGroup': 'PRODUCT',
        'callbackUrl': callback_url,
        'enabledInstallments': ['1', '2', '3', '6', '9'],

        'buyer': {
            'id': str(request.user.id),
            'name': siparis.ad,
            'surname': siparis.soyad,
            'gsmNumber': siparis.telefon or '+905555555555',
            'email': siparis.email,
            'identityNumber': siparis.tc_kimlik,  # GÜNCELLENDİ: Formdan gelen TC
            'lastLoginDate': timezone.now().strftime('%Y-%m-%d %H:%M:%S'),
            'registrationDate': request.user.date_joined.strftime('%Y-%m-%d %H:%M:%S'),
            'registrationAddress': siparis.adres,
            'ip': get_client_ip(request),
            'city': 'Istanbul',
            'country': 'Turkey',
            'zipCode': '34732'
        },
        'shippingAddress': {
            'contactName': f"{siparis.ad} {siparis.soyad}",
            'city': 'Istanbul',
            'country': 'Turkey',
            'address': siparis.adres,
            'zipCode': '34742'
        },
        'billingAddress': {
            'contactName': f"{siparis.ad} {siparis.soyad}",
            'city': 'Istanbul',
            'country': 'Turkey',
            'address': siparis.adres,
            'zipCode': '34742'
        },
        'basketItems': []
    }

    # --- KRİTİK DÜZELTME: Sepet Toplamı ve Ürün Fiyat Kontrolü ---
    iyzico_basket_items = []
    hesaplanan_toplam = Decimal('0.00')

    for item in siparis.items.all():
        item_price = item.fiyat * item.adet
        hesaplanan_toplam += item_price

        iyzico_basket_items.append({
            'id': str(item.kitap.id),
            'name': item.kitap.baslik,
            'category1': 'Kitap',
            'itemType': 'PHYSICAL',
            'price': str(item_price)
        })

    # Eğer kuruş farkı varsa, tek bir kalem olarak gönder (En güvenli yöntem)
    if hesaplanan_toplam != siparis.toplam_tutar:
        iyzico_basket_items = [{
            'id': str(siparis.id),
            'name': 'Siparis Toplami',
            'category1': 'Genel',
            'itemType': 'PHYSICAL',
            'price': str(siparis.toplam_tutar)
        }]

    request_iyzico['basketItems'] = iyzico_basket_items
    # --- DÜZELTME BİTİŞİ ---

    checkout_form_initialize = iyzipay.CheckoutFormInitialize()
    checkout_form_initialize_response = checkout_form_initialize.create(request_iyzico, options)

    if checkout_form_initialize_response['status'] == 'success':
        form_content = checkout_form_initialize_response['checkoutFormContent']
        return render(request, 'odeme/odeme_ekrani.html', {'iyzico_form': form_content})
    else:
        error_message = checkout_form_initialize_response.get('errorMessage', 'Bir hata oluştu')
        return HttpResponse(f"Ödeme başlatılamadı: {error_message} <br> <a href='/odeme/sepet/'>Sepete Dön</a>")


@csrf_exempt
def odeme_sonuc(request):
    """
    İyzico'nun POST ettiği sonucu karşılar.
    """
    if request.method == 'POST':
        token = request.POST.get('token')

        options = {
            'api_key': settings.IYZICO_API_KEY,
            'secret_key': settings.IYZICO_SECRET_KEY,
            'base_url': settings.IYZICO_BASE_URL
        }

        request_verification = {
            'locale': 'tr',
            'token': token
        }

        checkout_form = iyzipay.CheckoutForm()
        response = checkout_form.retrieve(request_verification, options)

        if response['status'] == 'success' and response['paymentStatus'] == 'SUCCESS':
            # Ödeme Başarılı
            siparis_id = response['basketId']
            islem_id = response['paymentId']

            try:
                siparis = Siparis.objects.get(id=siparis_id)
                siparis.odeme_tamamlandi = True
                siparis.iyzico_transaction_id = islem_id
                siparis.save()

                # Kupon kullanıldıysa kullanım sayısını artır
                sepet = _get_sepet(request)
                if sepet.uygulanan_kupon:
                    try:
                        kupon = IndirimKodu.objects.get(kod=siparis.kullanilan_kupon)
                        kupon.kullanim_sayisi += 1
                        kupon.save()
                    except IndirimKodu.DoesNotExist:
                        pass

                # Sepeti Temizle
                sepet.uygulanan_kupon = None
                sepet.save()
                sepet.items.all().delete()

                messages.success(request, "Ödemeniz başarıyla alındı. Siparişiniz hazırlanıyor.")
                return redirect('kullanicilar:hesabim')

            except Siparis.DoesNotExist:
                return HttpResponse("Sipariş bulunamadı.")

        else:
            # Ödeme Başarısız
            hata_mesaji = response.get('errorMessage', 'Ödeme alınamadı.')
            messages.error(request, f"Ödeme Başarısız: {hata_mesaji}")
            return redirect('odeme:sepeti_goruntule')

    return redirect('anasayfa')


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
