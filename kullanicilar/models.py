# kullanicilar/models.py
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Profil(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    telefon = models.CharField(max_length=15, blank=True, verbose_name="Telefon Numarası")
    onaylandi = models.BooleanField(default=True, verbose_name="Hesap Onaylandı")
    kayit_tarihi = models.DateTimeField(default=timezone.now)
    ozel_erisim = models.BooleanField(default=False, verbose_name="Özel Erişim") # Yeni Alan

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = "Kullanıcı Profili"
        verbose_name_plural = "Kullanıcı Profilleri"
