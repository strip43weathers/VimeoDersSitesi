# blog/admin.py
from django.contrib import admin
from .models import BlogYazisi

@admin.register(BlogYazisi)
class BlogYazisiAdmin(admin.ModelAdmin):
    list_display = ('baslik', 'sira_numarasi', 'olusturulma_tarihi')
    list_editable = ('sira_numarasi',)

#bsb
