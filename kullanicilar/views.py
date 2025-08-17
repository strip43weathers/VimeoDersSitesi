from django.shortcuts import render, redirect
from .forms import KayitFormu
from .models import Profil
from django.contrib import messages


def kayit_view(request):
    if request.method == 'POST':
        form = KayitFormu(request.POST)
        if form.is_valid():
            user = form.save()

            Profil.objects.create(user=user, onaylandi=False)
            messages.success(request, 'Tebrikler başarıyla kaydoldunuz. Yönetici hesabınızı onayladıktan sonra giriş yapabileceksiniz.')

            return redirect('login')
    else:
        form = KayitFormu()
    return render(request, 'registration/kayit.html', {'form': form})
