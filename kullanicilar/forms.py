from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

class KayitFormu(UserCreationForm):
    email = forms.EmailField(required=True, help_text="Lütfen geçerli bir e-posta adresi girin.")

    # Bu __init__ metodu, formun alanlarını Türkçeleştirmek için eklendi.
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = "Kullanıcı Adı"
        self.fields['username'].help_text = "En fazla 150 karakter. Sadece harf, rakam ve @/./+/-/_ karakterleri."
        self.fields['first_name'].label = "Adınız"
        self.fields['last_name'].label = "Soyadınız"
        self.fields['password1'].label = "Parola"
        self.fields['password2'].label = "Parola (Tekrar)"

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('first_name', 'last_name', 'email')


class CustomAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = "Kullanıcı Adı"
        self.fields['password'].label = "Parola"

    error_messages = {
        'invalid_login': (
            "Kullanıcı adı veya parolanız hatalı. "
            "Not: Hesabınız henüz yönetici tarafından onaylanmamış olabilir."
        ),
        'inactive': ("Bu hesap aktif değil."),
    }
