from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

class KayitFormu(UserCreationForm):
    email = forms.EmailField(required=True, help_text="Lütfen geçerli bir e-posta adresi girin.")
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