from django.contrib import admin
from .models import Kurs, Ders

# Kurs modeli için gelişmiş admin arayüzünü tanımlıyoruz
class KursAdmin(admin.ModelAdmin):
    list_display = ('baslik', 'herkese_acik', 'olusturulma_tarihi')
    list_filter = ('herkese_acik',)
    search_fields = ('baslik', 'aciklama')
    # ManyToMany alanları için en kullanışlı arayüzü sağlar
    filter_horizontal = ('izinli_kullanicilar',)

# Modellerimizi admin paneline kaydediyoruz
# Kurs modelini, yukarıda tanımladığımız özel arayüz ile kaydediyoruz
admin.site.register(Kurs, KursAdmin)
admin.site.register(Ders)
