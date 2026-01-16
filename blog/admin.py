from django.contrib import admin
from .models import BlogYazisi

@admin.register(BlogYazisi)
class BlogYazisiAdmin(admin.ModelAdmin):
    list_display = ('baslik', 'sira_numarasi', 'olusturulma_tarihi', 'seo_durumu')
    list_editable = ('sira_numarasi',)
    search_fields = ('baslik', 'seo_title')
    prepopulated_fields = {'slug': ('baslik',)}

    # --- PANELİ GRUPLARA AYIRAN KISIM ---
    fieldsets = (
        ('İçerik Bilgileri', {
            'fields': ('baslik', 'slug', 'icerik', 'sira_numarasi')
        }),
        ('SEO ve Kapak Görseli (Google Ayarları)', {
            'fields': ('gorsel', 'gorsel_alt_metni', 'seo_title', 'meta_description'),
            'description': 'Bu alandaki bilgiler Google arama sonuçlarında görünür.'
        }),
    )

    def seo_durumu(self, obj):
        if obj.seo_title and obj.meta_description:
            return "✅ SEO Girildi"
        return "❌ Eksik"
    seo_durumu.short_description = "SEO Kontrol"
