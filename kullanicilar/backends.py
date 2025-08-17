from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User


class OnayliKullaniciBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):

        user = super().authenticate(request, username, password, **kwargs)

        if user is None:
            return None

        try:
            if user.profil.onaylandi:
                return user
        except user._meta.model.profil.RelatedObjectDoesNotExist:

            if user.is_superuser:
                return user

        return None
