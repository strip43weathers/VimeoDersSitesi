# dosya: sayfalar/admin.py
from django.contrib import admin
from .models import Sayfa

@admin.register(Sayfa)
class SayfaAdmin(admin.ModelAdmin):
    list_display = ('baslik', 'slug', 'guncellenme_tarihi')
    search_fields = ('baslik', 'icerik')
    prepopulated_fields = {'slug': ('baslik',)} # Başlığa göre slug'ı otomatik doldurur