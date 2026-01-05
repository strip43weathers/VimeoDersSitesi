# odeme/admin.py

from django.contrib import admin, messages
from django.utils.html import format_html
from django.urls import path, reverse
from django.shortcuts import redirect, get_object_or_404
from django.db import transaction
from django.db.models import F

# Modeller
from .models import Kitap, Sepet, SepetUrunu, Siparis, SiparisUrunu, IndirimKodu, KitapGorsel, KitapVideo
# Servis (Sorgulama işlemi için gerekli)
from .services import IyzicoService


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
    # 1. 'iyzico_kontrol_butonu'nu listeye ekledik.
    list_display = (
        'id',
        'user',
        'ad',
        'soyad',
        'toplam_tutar',
        'odeme_tamamlandi',
        'durum',
        'tarih',
        'iyzico_kontrol_butonu'  # <--- YENİ EKLENEN BUTON
    )

    list_filter = ('odeme_tamamlandi', 'durum', 'tarih')

    search_fields = (
        'ad',
        'soyad',
        'email',
        'telefon',
        'user__username',
        'kargo_takip_no',
        'kullanilan_kupon',
        'iyzico_transaction_id'
    )

    inlines = [SiparisUrunuInline]

    # İyzico ID'si ve buton elle değiştirilmesin
    readonly_fields = ('tarih', 'toplam_tutar', 'kullanilan_kupon', 'iyzico_transaction_id')

    list_editable = ('durum',)

    # --- ÖZEL BUTON VE AKSİYONLAR ---

    def iyzico_kontrol_butonu(self, obj):
        """
        Eğer ödeme tamamlanmadıysa, admin panelinde 'Sorgula' butonu gösterir.
        """
        if not obj.odeme_tamamlandi:
            return format_html(
                '<a class="button" style="background-color: #ba2121; color: white; padding: 3px 10px; border-radius: 5px;" href="{}">İyzico Sorgula</a>',
                reverse('admin:siparis_sorgula', args=[obj.pk])
            )
        return format_html('<span style="color: green;">✔ Onaylı</span>')

    iyzico_kontrol_butonu.short_description = "Ödeme Kontrol"
    iyzico_kontrol_butonu.allow_tags = True

    def get_urls(self):
        """
        Özel butonun çalışması için URL tanımlaması.
        """
        urls = super().get_urls()
        custom_urls = [
            path(
                '<int:siparis_id>/sorgula/',
                self.admin_site.admin_view(self.admin_siparis_sorgula),
                name='siparis_sorgula',
            ),
        ]
        return custom_urls + urls

    def admin_siparis_sorgula(self, request, siparis_id):
        """
        Butona basıldığında çalışacak mantık.
        İyzico servisine gidip durumu sorar ve gerekirse siparişi kurtarır.
        """
        siparis = get_object_or_404(Siparis, id=siparis_id)

        # 1. Servis Çağrısı (Services.py'ye eklediğin yeni metodu kullanır)
        sonuc = IyzicoService.siparis_durumu_sorgula(siparis.id)

        if sonuc.get('status') == 'success' and sonuc.get('paymentStatus') == 'SUCCESS':
            islem_id = sonuc.get('paymentId', '')

            try:
                with transaction.atomic():
                    # Siparişi kilitle
                    s_locked = Siparis.objects.select_for_update().get(id=siparis.id)

                    if s_locked.odeme_tamamlandi:
                        self.message_user(request, "Bu sipariş zaten onaylanmış.", messages.WARNING)
                        return redirect('admin:odeme_siparis_changelist')

                    # --- STOK KONTROLÜ ---
                    stok_yetersiz = False
                    eksik_urunler = []

                    for item in s_locked.items.all():
                        kitap = Kitap.objects.select_for_update().get(id=item.kitap.id)
                        if kitap.stok < item.adet:
                            stok_yetersiz = True
                            eksik_urunler.append(kitap.baslik)

                    if stok_yetersiz:
                        s_locked.odeme_tamamlandi = True
                        s_locked.iyzico_transaction_id = islem_id
                        s_locked.durum = 'stok_hatasi'
                        s_locked.save()
                        self.message_user(request, f"Ödeme bulundu ANCAK STOK YOK! Sipariş 'Stok Hatası'na çekildi. Eksikler: {eksik_urunler}", messages.ERROR)
                    else:
                        # Stokları düş
                        for item in s_locked.items.all():
                            kitap = Kitap.objects.get(id=item.kitap.id)
                            kitap.stok -= item.adet
                            kitap.save()

                        # Siparişi onayla
                        s_locked.odeme_tamamlandi = True
                        s_locked.iyzico_transaction_id = islem_id
                        s_locked.durum = 'hazirlaniyor'
                        s_locked.save()

                        # Sepet Temizliği (Opsiyonel ama iyi olur)
                        try:
                            sepet = Sepet.objects.filter(user=s_locked.user).first()
                            if sepet:
                                if sepet.uygulanan_kupon:
                                    IndirimKodu.objects.filter(id=sepet.uygulanan_kupon.id).update(
                                        kullanim_sayisi=F('kullanim_sayisi') + 1
                                    )
                                sepet.uygulanan_kupon = None
                                sepet.save()
                                sepet.items.all().delete()
                        except Exception:
                            pass

                        self.message_user(request, f"Sipariş #{siparis.id} İyzico üzerinden başarıyla DOĞRULANDI ve ONAYLANDI.", messages.SUCCESS)

            except Exception as e:
                self.message_user(request, f"İşlem sırasında veritabanı hatası oluştu: {e}", messages.ERROR)

        else:
            hata_mesaji = sonuc.get('errorMessage', 'Ödeme bulunamadı')
            self.message_user(request, f"İyzico'da bu sipariş için başarılı bir ödeme GÖRÜNMÜYOR. İyzico Mesajı: {hata_mesaji}", messages.WARNING)

        return redirect('admin:odeme_siparis_changelist')


# --- KİTAP DETAYLARI İÇİN INLINE YAPILARI ---

class KitapGorselInline(admin.TabularInline):
    model = KitapGorsel
    extra = 1  # Yeni ekleme için boş satır sayısı
    verbose_name = "Ekstra Görsel"
    verbose_name_plural = "Galeri Görselleri"


class KitapVideoInline(admin.TabularInline):
    model = KitapVideo
    extra = 1
    verbose_name = "Video"
    verbose_name_plural = "Tanıtım Videoları"


# --- KİTAP ADMIN (GÜNCELLENMİŞ) ---

@admin.register(Kitap)
class KitapAdmin(admin.ModelAdmin):
    list_display = ('baslik', 'fiyat', 'stok', 'sira')
    list_editable = ('fiyat', 'stok', 'sira')
    search_fields = ('baslik',)

    # İşte burası resim ve videoları kitap sayfasında yönetmenizi sağlar
    inlines = [KitapGorselInline, KitapVideoInline]
