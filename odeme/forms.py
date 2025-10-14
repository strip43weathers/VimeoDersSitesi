# odeme/forms.py

from django import forms
from .models import SinavSiparisi, PaketSiparisi, KitapSiparisi


# Mevcut Sınav Sipariş Formu (eğer kullanıyorsanız)
class SiparisForm(forms.ModelForm):
    sozlesme_onay = forms.BooleanField(required=True, label='')

    class Meta:
        model = SinavSiparisi
        fields = ['ad', 'soyad', 'email', 'telefon', 'adres']


# Yeni Paket Sipariş Formu
class PaketSiparisForm(forms.ModelForm):
    class Meta:
        model = PaketSiparisi
        fields = ['ad', 'soyad', 'email', 'telefon', 'adres']


class KitapSiparisForm(forms.ModelForm):
    class Meta:
        model = KitapSiparisi
        fields = ['ad', 'soyad', 'email', 'telefon', 'adres']