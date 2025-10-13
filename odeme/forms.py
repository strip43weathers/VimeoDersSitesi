# odeme/forms.py

from django import forms
from .models import SinavSiparisi, PaketSiparisi # PaketSiparisi modelini import et

# Mevcut Sınav Sipariş Formu (eğer kullanıyorsanız)
class SiparisForm(forms.ModelForm):
    class Meta:
        model = SinavSiparisi
        fields = ['ad', 'soyad', 'email', 'telefon', 'adres']

# Yeni Paket Sipariş Formu
class PaketSiparisForm(forms.ModelForm):
    class Meta:
        model = PaketSiparisi
        fields = ['ad', 'soyad', 'email', 'telefon', 'adres']
