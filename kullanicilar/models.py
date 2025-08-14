from django.db import models
from django.contrib.auth.models import User

class Profil(models.Model):
    # Her Profil, bir User (kullanıcı) ile bire-bir eşleşecek.
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # İşte sihirli alanımız: Bu alan, hesabın onaylanıp onaylanmadığını tutacak.
    onaylandi = models.BooleanField(default=False, verbose_name="Hesap Onaylandı")

    def __str__(self):
        return self.user.username # Admin panelinde daha okunaklı görünmesi için.

    class Meta:
        verbose_name = "Kullanıcı Profili"
        verbose_name_plural = "Kullanıcı Profilleri"