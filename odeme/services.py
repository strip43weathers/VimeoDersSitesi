# odeme/services.py

import iyzipay
import json
from decimal import Decimal
from django.conf import settings
from django.utils import timezone


class IyzicoService:
    @staticmethod
    def get_options():
        """
        API anahtarlarını ve URL'yi settings'den alır ve temizler.
        """
        api_key = str(settings.IYZICO_API_KEY).replace("'", "").replace('"', "").strip()
        secret_key = str(settings.IYZICO_SECRET_KEY).replace("'", "").replace('"', "").strip()
        base_url = str(settings.IYZICO_BASE_URL).replace("'", "").replace('"', "").strip()

        # URL Temizliği
        if base_url.startswith("https://"):
            base_url = base_url.replace("https://", "")
        if base_url.startswith("http://"):
            base_url = base_url.replace("http://", "")

        base_url = base_url.rstrip('/')

        options = {
            'api_key': api_key,
            'secret_key': secret_key,
            'base_url': base_url
        }
        return options

    @staticmethod
    def create_checkout_form(siparis, user, ip, callback_url):
        """
        Sipariş için ödeme formunu başlatır.
        """
        options = IyzicoService.get_options()

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
                'id': str(user.id),
                'name': siparis.ad,
                'surname': siparis.soyad,
                'gsmNumber': siparis.telefon,
                'email': siparis.email,
                'identityNumber': siparis.tc_kimlik,
                'lastLoginDate': timezone.now().strftime('%Y-%m-%d %H:%M:%S'),
                'registrationDate': user.date_joined.strftime('%Y-%m-%d %H:%M:%S'),
                'registrationAddress': siparis.adres,
                'ip': ip,
                'city': siparis.sehir,
                'country': siparis.ulke,
                'zipCode': siparis.posta_kodu,
            },
            'shippingAddress': {
                'contactName': f"{siparis.ad} {siparis.soyad}",
                'city': siparis.sehir,
                'country': siparis.ulke,
                'address': siparis.adres,
                'zipCode': siparis.posta_kodu,
            },
            'billingAddress': {
                'contactName': f"{siparis.ad} {siparis.soyad}",
                'city': siparis.ulke,
                'country': siparis.ulke,
                'address': siparis.adres,
                'zipCode': siparis.posta_kodu,
            },
            'basketItems': []
        }

        # Sepet Kalemlerini Ekle
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

        # Kuruş farkı kontrolü
        if hesaplanan_toplam != siparis.toplam_tutar:
            iyzico_basket_items = [{
                'id': str(siparis.id),
                'name': 'Siparis Toplami',
                'category1': 'Genel',
                'itemType': 'PHYSICAL',
                'price': str(siparis.toplam_tutar)
            }]

        request_iyzico['basketItems'] = iyzico_basket_items

        # İsteği Gönder
        checkout_form_initialize = iyzipay.CheckoutFormInitialize()
        raw_response = checkout_form_initialize.create(request_iyzico, options)

        # Yanıtı işle ve döndür
        try:
            content = raw_response.read().decode('utf-8')
            return json.loads(content)
        except Exception as e:
            return {'status': 'failure', 'errorMessage': f'JSON Decode Hatası: {str(e)}'}

    @staticmethod
    def retrieve_checkout_form_result(token):
        """
        Ödeme sonucunu İyzico'dan sorgular.
        """
        options = IyzicoService.get_options()
        request = {
            'locale': 'tr',
            'token': token
        }

        checkout_form = iyzipay.CheckoutForm()
        raw_response = checkout_form.retrieve(request, options)

        try:
            content = raw_response.read().decode('utf-8')
            return json.loads(content)
        except Exception as e:
            return {'status': 'failure', 'errorMessage': f'JSON Decode Hatası: {str(e)}'}
