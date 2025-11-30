# odeme/admin.py

from django.contrib import admin
from .models import Kitap, EgitimPaketi, Sepet, SepetUrunu, Siparis, SiparisUrunu

# --- SEPET ADMIN ---
class SepetUrunuInline(admin.TabularInline):
    model = SepetUrunu
    extra = 0
    readonly_fields = ('toplam_fiyat',)

@admin.register(Sepet)
class SepetAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'session_key', 'olusturulma_tarihi', 'urun_sayisi', 'toplam_tutar')
    search_fields = ('user__username', 'session_key')
    inlines = [SepetUrunuInline]

# --- SİPARİŞ ADMIN ---
class SiparisUrunuInline(admin.TabularInline):
    model = SiparisUrunu
    extra = 0
    readonly_fields = ('fiyat',) # Fiyat sonradan değişmemeli

@admin.register(Siparis)
class SiparisAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'ad', 'soyad', 'toplam_tutar', 'durum', 'tarih')
    list_filter = ('durum', 'tarih')
    search_fields = ('ad', 'soyad', 'email', 'telefon', 'user__username', 'kargo_takip_no')
    inlines = [SiparisUrunuInline]
    readonly_fields = ('tarih', 'toplam_tutar')
    list_editable = ('durum',) # Durumu liste üzerinden hızlıca değiştirebilmek için

# --- DİĞER ---
admin.site.register(Kitap)
admin.site.register(EgitimPaketi)