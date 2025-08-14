from django.shortcuts import render, redirect
from .forms import KayitFormu
from .models import Profil

def kayit_view(request):
    if request.method == 'POST':
        form = KayitFormu(request.POST)
        if form.is_valid():
            user = form.save()
            # Yeni bir kullanıcı oluştuğunda, ona otomatik olarak
            # onaylanmamış bir profil de oluşturuyoruz.
            Profil.objects.create(user=user, onaylandi=False)
            # Başarılı kayıttan sonra öğrenciyi bilgilendirme amaçlı
            # giriş sayfasına yönlendiriyoruz.
            return redirect('login')
    else:
        form = KayitFormu()
    return render(request, 'registration/kayit.html', {'form': form})