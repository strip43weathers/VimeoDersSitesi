from django.db import models
from django.contrib.auth.models import User


class Profil(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    onaylandi = models.BooleanField(default=False, verbose_name="Hesap Onaylandı")

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = "Kullanıcı Profili"
        verbose_name_plural = "Kullanıcı Profilleri"
