# dosya: oyunlar/admin.py
from django.contrib import admin
from .models import Oyun

@admin.register(Oyun)
class OyunAdmin(admin.ModelAdmin):
    list_display = ('baslik', 'sira_numarasi', 'sadece_uyelere_ozel')
    list_editable = ('sira_numarasi', 'sadece_uyelere_ozel')
    list_filter = ('sadece_uyelere_ozel',) # Filtreleme ekleyelim