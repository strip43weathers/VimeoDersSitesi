# odeme/admin.py

from django.contrib import admin
from .models import Sinav, SinavSiparisi, EgitimPaketi, PaketSiparisi, Kitap, KitapSiparisi


# --- MEVCUT KAYITLAR ---
class SinavSiparisiAdmin(admin.ModelAdmin):
    list_display = ('user', 'sinav', 'ad', 'soyad', 'email', 'tarih', 'odeme_tamamlandi')
    list_filter = ('odeme_tamamlandi',)
    search_fields = ('user__username', 'ad', 'soyad')
    readonly_fields = ('user', 'sinav', 'tarih')


admin.site.register(Kitap)
admin.site.register(KitapSiparisi)


admin.site.register(Sinav)
admin.site.register(SinavSiparisi, SinavSiparisiAdmin)


# --- YENİ EKLENEN KAYITLAR ---
class PaketSiparisiAdmin(admin.ModelAdmin):
    list_display = ('user', 'paket', 'ad', 'soyad', 'email', 'tarih', 'odeme_tamamlandi')
    list_filter = ('odeme_tamamlandi', 'paket')
    search_fields = ('user__username', 'ad', 'soyad', 'email')
    readonly_fields = ('user', 'paket', 'tarih')

admin.site.register(EgitimPaketi)
admin.site.register(PaketSiparisi, PaketSiparisiAdmin)
