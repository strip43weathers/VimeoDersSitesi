# sayfalar/forms.py

from django import forms
from .models import IletisimTalebi

class IletisimForm(forms.ModelForm):
    class Meta:
        model = IletisimTalebi
        fields = ['ad_soyad', 'email', 'telefon', 'mesaj']
        widgets = {
            'ad_soyad': forms.TextInput(attrs={
                'class': 'form-control bg-light border-0', # bg-light ve border-0 daha modern bir hava katar
                'placeholder': 'Ad Soyad',
                'style': 'height: 55px;' # Floating label için yükseklik ayarı
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control bg-light border-0',
                'placeholder': 'E-posta',
                'style': 'height: 55px;'
            }),
            'telefon': forms.TextInput(attrs={
                'class': 'form-control bg-light border-0',
                'placeholder': 'Telefon',
                'style': 'height: 55px;'
            }),
            'mesaj': forms.Textarea(attrs={
                'class': 'form-control bg-light border-0',
                'placeholder': 'Mesajınız',
                'style': 'height: 150px;', # Mesaj kutusu daha yüksek olsun
                'rows': 4
            }),
        }
