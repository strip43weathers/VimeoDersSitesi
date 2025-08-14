from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class KayitFormu(UserCreationForm):
    email = forms.EmailField(required=True, help_text="Lütfen geçerli bir e-posta adresi girin.")

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('first_name', 'last_name', 'email')