# dosya: dersler/admin.py

from django.contrib import admin
from .models import Kurs, Ders

class DersAdmin(admin.ModelAdmin):
    list_display = ('baslik', 'kurs', 'sira_numarasi')
    list_filter = ('kurs',)
    search_fields = ('baslik', 'aciklama')


class KursAdmin(admin.ModelAdmin):
    list_display = ('baslik', 'herkese_acik', 'olusturulma_tarihi')
    list_filter = ('herkese_acik',)
    search_fields = ('baslik', 'aciklama')
    filter_horizontal = ('izinli_kullanicilar',)

admin.site.register(Kurs, KursAdmin)
admin.site.register(Ders, DersAdmin)
