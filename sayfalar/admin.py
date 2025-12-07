# dosya: sayfalar/admin.py
from django.contrib import admin
from .models import Sayfa, RehberVideo, IletisimTalebi

@admin.register(Sayfa)
class SayfaAdmin(admin.ModelAdmin):
    list_display = ('baslik', 'slug', 'guncellenme_tarihi')
    search_fields = ('baslik', 'icerik')
    prepopulated_fields = {'slug': ('baslik',)}

@admin.register(RehberVideo)
class RehberVideoAdmin(admin.ModelAdmin):
    # 'sayfa' alanını listeye ekleyelim
    list_display = ('baslik', 'sayfa', 'vimeo_video_id', 'aktif')
    # Sayfaya göre filtreleme seçeneği ekleyelim
    list_filter = ('sayfa', 'aktif')


@admin.register(IletisimTalebi)
class IletisimTalebiAdmin(admin.ModelAdmin):
    list_display = ('ad_soyad', 'telefon', 'email', 'olusturulma_tarihi')
    list_filter = ('olusturulma_tarihi',)
    search_fields = ('ad_soyad', 'telefon', 'email')
    readonly_fields = ('olusturulma_tarihi',) # Tarih değiştirilemesin