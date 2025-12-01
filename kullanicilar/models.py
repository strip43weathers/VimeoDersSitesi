# kullanicilar/models.py
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import datetime


class Profil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profil')  # related_name ekledik
    telefon = models.CharField(max_length=15, blank=True, verbose_name="Telefon Numarası")
    onaylandi = models.BooleanField(default=True, verbose_name="Hesap Onaylandı")
    kayit_tarihi = models.DateTimeField(default=timezone.now)
    ozel_erisim = models.BooleanField(default=False, verbose_name="Özel Erişim")

    def __str__(self):
        return self.user.username

    def erisim_izni_var_mi(self):
        """Kullanıcının içeriklere erişim izni olup olmadığını kontrol eder."""
        # 1. Özel erişim yetkisi var mı?
        if self.ozel_erisim:
            return True

        # 2. Eski kullanıcı mı? (25 Ekim 2025'ten önce kayıt olanlar)
        # Not: Bu tarihi settings.py'dan çekmek daha iyidir ama şimdilik burada kalsın.
        gecis_tarihi = timezone.make_aware(datetime.datetime(2025, 10, 25))
        if self.user.date_joined < gecis_tarihi:
            return True

        return False

    class Meta:
        verbose_name = "Kullanıcı Profili"
        verbose_name_plural = "Kullanıcı Profilleri"
