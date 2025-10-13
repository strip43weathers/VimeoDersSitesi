# odeme/forms.py

from django import forms
from .models import SinavSiparisi

class SiparisForm(forms.ModelForm):
    class Meta:
        model = SinavSiparisi
        fields = ['ad', 'soyad', 'email', 'telefon', 'adres']
