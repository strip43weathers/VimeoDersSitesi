# odeme/admin.py

from django.contrib import admin
from .models import Kitap, Sepet, SepetUrunu, Siparis, SiparisUrunu, IndirimKodu


# --- KUPON ADMIN ---

@admin.register(IndirimKodu)
class IndirimKoduAdmin(admin.ModelAdmin):
    list_display = ('kod', 'indirim_orani', 'kullanim_durumu', 'gecerlilik_tarihi', 'aktif', 'gecerlilik_durumu')
    list_filter = ('aktif', 'gecerlilik_tarihi')
    search_fields = ('kod',)
    list_editable = ('aktif',)
    ordering = ('-gecerlilik_tarihi',)

    # Detay sayfasında kullanım sayısı değiştirilemez olsun (güvenlik için)
    readonly_fields = ('kullanim_sayisi',)

    def gecerlilik_durumu(self, obj):
        return obj.gecerli_mi

    gecerlilik_durumu.boolean = True
    gecerlilik_durumu.short_description = "Geçerli mi?"

    def kullanim_durumu(self, obj):
        if obj.kullanim_limiti == 0:
            return f"{obj.kullanim_sayisi} / ∞"
        return f"{obj.kullanim_sayisi} / {obj.kullanim_limiti}"

    kullanim_durumu.short_description = "Kullanım (Adet / Limit)"


# --- SEPET ADMIN ---

class SepetUrunuInline(admin.TabularInline):
    model = SepetUrunu
    extra = 0
    readonly_fields = ('toplam_fiyat',)


@admin.register(Sepet)
class SepetAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'session_key', 'olusturulma_tarihi', 'urun_sayisi', 'toplam_tutar', 'uygulanan_kupon')
    search_fields = ('user__username', 'session_key')
    list_filter = ('olusturulma_tarihi',)
    inlines = [SepetUrunuInline]


# --- SİPARİŞ ADMIN ---

class SiparisUrunuInline(admin.TabularInline):
    model = SiparisUrunu
    extra = 0
    readonly_fields = ('fiyat',)


@admin.register(Siparis)
class SiparisAdmin(admin.ModelAdmin):
    # 1. 'odeme_tamamlandi' alanını listeye ekledik.
    # Django bunu otomatik olarak yeşil tik veya kırmızı çarpı ikonu olarak gösterir.
    list_display = (
        'id',
        'user',
        'ad',
        'soyad',
        'toplam_tutar',
        'odeme_tamamlandi',  # <--- BURASI EKLENDİ (Ödeme Durumu Sütunu)
        'durum',
        'tarih'
    )

    # 2. Yan panele filtreleme ekledik.
    # Artık sağ taraftan "Evet"i seçip sadece parası alınanları görebilirsin.
    list_filter = ('odeme_tamamlandi', 'durum', 'tarih')  # <--- BURASI GÜNCELLENDİ

    # 3. İyzico işlem numarasına göre arama yapabilmek için ekleme yaptık.
    search_fields = (
        'ad',
        'soyad',
        'email',
        'telefon',
        'user__username',
        'kargo_takip_no',
        'kullanilan_kupon',
        'iyzico_transaction_id'  # <--- EKLENDİ (İşlem no ile arama)
    )

    inlines = [SiparisUrunuInline]

    # İyzico ID'si elle değiştirilmesin diye readonly yaptık.
    readonly_fields = ('tarih', 'toplam_tutar', 'kullanilan_kupon', 'iyzico_transaction_id')

    list_editable = ('durum',)


# --- DİĞER ---
admin.site.register(Kitap)
