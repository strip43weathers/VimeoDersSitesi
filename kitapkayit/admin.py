# kitapkayit/admin.py
from django.contrib import admin
from .models import KitapKaydi

@admin.register(KitapKaydi)
class KitapKaydiAdmin(admin.ModelAdmin):
    list_display = ('isim', 'soyisim', 'email', 'telefon', 'kayit_tarihi')
    search_fields = ('isim', 'soyisim', 'email', 'telefon')
    list_filter = ('kayit_tarihi',)
