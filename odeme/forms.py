# odeme/forms.py

from django import forms
from .models import Siparis


class SiparisForm(forms.ModelForm):
    sozlesme_onay = forms.BooleanField(
        required=True,
        label="Satış Sözleşmesi'ni okudum ve kabul ediyorum."
    )
    teslimat_ve_iade_onay = forms.BooleanField(
        required=True,
        label="Teslimat ve İade Şartları'nı okudum ve kabul ediyorum."
    )

    class Meta:
        model = Siparis
        fields = ['ad', 'soyad', 'email', 'telefon', 'tc_kimlik', 'sehir', 'posta_kodu', 'ulke', 'adres']
        widgets = {
            'adres': forms.Textarea(attrs={'rows': 3}),
        }


class IndirimKoduForm(forms.Form):
    kod = forms.CharField(
        max_length=50,
        label='İndirim Kodu',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Kupon Kodu'})
    )


#a