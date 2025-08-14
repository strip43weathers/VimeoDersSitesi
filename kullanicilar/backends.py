from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User

class OnayliKullaniciBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        # Önce Django'nun normal şifre kontrolünü yapmasını sağlıyoruz
        user = super().authenticate(request, username, password, **kwargs)

        # Eğer kullanıcı adı/şifre yanlışsa veya kullanıcı yoksa, user None döner.
        # Bu durumda biz de None dönerek girişi engelliyoruz.
        if user is None:
            return None

        # Eğer şifre doğruysa, şimdi kendi özel kontrolümüzü yapıyoruz:
        # Kullanıcının profili var mı ve onaylanmış mı?
        try:
            if user.profil.onaylandi:
                return user # Profil onaylı ise, kullanıcıyı döndürerek girişe izin ver.
        except user._meta.model.profil.RelatedObjectDoesNotExist:
            # Eğer kullanıcının profili yoksa (örneğin ilk oluşturduğumuz superuser gibi),
            # ve bu kullanıcı bir admin ise, girişine izin ver.
            if user.is_superuser:
                return user

        # Yukarıdaki şartların hiçbiri sağlanmazsa (yani profili var ama onaylı değilse),
        # None döndürerek girişi engelle.
        return None