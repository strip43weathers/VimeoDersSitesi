from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordResetForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class KayitFormu(UserCreationForm):
    email = forms.EmailField(required=True, help_text="Lütfen geçerli bir e-posta adresi girin.")

    # Bu __init__ metodu, formun alanlarını Türkçeleştirmek için eklendi.
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = "Kullanıcı Adı"
        self.fields['username'].help_text = "Herkesten farklı olmak zorunda. En fazla 150 karakter. Sadece harf, rakam ve @ / . / + / - / _ karakterleri."
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
            "Kullanıcı Adı veya Parolanız hatalı. Lütfen tekrar deneyiniz. Not: Yönetici henüz hesabınızı onaylamamış olabilir. "
        ),
        'inactive': ("Bu hesap aktif değil."),
    }

class CustomPasswordResetForm(PasswordResetForm):
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email:
            try:
                # E-posta adresine sahip bir kullanıcı var mı diye kontrol et
                user = User.objects.get(email__iexact=email)
                # Kullanıcının profili var mı ve onaylanmış mı diye kontrol et
                if not hasattr(user, 'profil') or not user.profil.onaylandi:
                    # Onaylanmamışsa, özel hata mesajımızı göster
                    raise ValidationError(
                        "Şifremi unuttum seçeneğini kullanabilmeniz için hesabınızın yönetici tarafından onaylanmış olması gerekir.",
                        code='unapproved_account'
                    )
            except User.DoesNotExist:
                # E-posta adresi sistemde yoksa, Django'nun varsayılan davranışını sürdür
                # (güvenlik nedeniyle kullanıcıya bilgi verilmez).
                pass
        return email