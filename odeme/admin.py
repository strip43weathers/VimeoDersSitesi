# odeme/admin.py

from django.contrib import admin
from .models import Sinav, SinavSiparisi

# Sınav Siparişlerini admin panelinde daha okunaklı göstermek için
class SinavSiparisiAdmin(admin.ModelAdmin):
    list_display = ('user', 'sinav', 'ad', 'soyad', 'email', 'tarih', 'odeme_tamamlandi')
    list_filter = ('odeme_tamamlandi',)
    search_fields = ('user__username', 'ad', 'soyad', 'email')
    readonly_fields = ('user', 'sinav', 'tarih')

# Modelleri admin paneline kaydediyoruz
admin.site.register(Sinav)
admin.site.register(SinavSiparisi, SinavSiparisiAdmin)
