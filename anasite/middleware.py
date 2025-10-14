# anasite/middleware.py

import base64
from django.http import HttpResponse
from django.conf import settings
from django.urls import reverse


class BasicAuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Ayarlarda koruma aktif değilse veya kullanıcı zaten admin paneline giriş yapmışsa,
        # bu adımı atla.
        if not getattr(settings, 'BASIC_AUTH_ENABLED', False) or (
                request.user.is_authenticated and request.user.is_staff):
            return self.get_response(request)

        # Admin giriş sayfasını korumadan muaf tut.
        admin_login_url = reverse('admin:login')
        if request.path.startswith(admin_login_url):
            return self.get_response(request)

        # Tarayıcıdan gelen yetkilendirme bilgisini kontrol et.
        if 'HTTP_AUTHORIZATION' in request.META:
            auth = request.META['HTTP_AUTHORIZATION'].split()
            if len(auth) == 2 and auth[0].lower() == "basic":
                try:
                    user, passwd = base64.b64decode(auth[1]).decode('utf-8').split(':', 1)

                    if user == settings.BASIC_AUTH_USER and passwd == settings.BASIC_AUTH_PASSWORD:
                        return self.get_response(request)
                except Exception:
                    pass

        # Yetkilendirme başarısız olursa 401 yanıtı gönder.
        response = HttpResponse("Authorization Required", status=401)
        # --- DEĞİŞİKLİK BU SATIRDA ---
        response['WWW-Authenticate'] = 'Basic realm="Restricted Area"'
        return response