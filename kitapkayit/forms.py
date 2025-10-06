# kitapkayit/forms.py
from django import forms
from .models import KitapKaydi

class KitapKayitForm(forms.ModelForm):
    class Meta:
        model = KitapKaydi
        fields = ['isim', 'soyisim', 'email', 'telefon']

    def __init__(self, *args, **kwargs):
        super(KitapKayitForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
