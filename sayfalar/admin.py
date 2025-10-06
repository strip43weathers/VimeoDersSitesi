# dosya: sayfalar/admin.py
from django.contrib import admin
from .models import Sayfa, RehberVideo

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
