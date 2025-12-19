# kullanicilar/models.py
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import datetime
from django.conf import settings
from django.utils.dateparse import parse_datetime

class Profil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profil')  # related_name ekledik
    telefon = models.CharField(max_length=15, blank=True, verbose_name="Telefon Numarası")
    onaylandi = models.BooleanField(default=True, verbose_name="Hesap Onaylandı")
    kayit_tarihi = models.DateTimeField(default=timezone.now)
    ozel_erisim = models.BooleanField(default=False, verbose_name="Özel Erişim")

    def __str__(self):
        return self.user.username

    def erisim_izni_var_mi(self):

        return self.ozel_erisim

    class Meta:
        verbose_name = "Kullanıcı Profili"
        verbose_name_plural = "Kullanıcı Profilleri"
