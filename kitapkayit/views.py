# kitapkayit/views.py
from django.shortcuts import render, redirect
from .forms import KitapKayitForm

def kitap_kayit_view(request):
    if request.method == 'POST':
        form = KitapKayitForm(request.POST)
        if form.is_valid():
            form.save()
            # Kayıt başarılı olunca 'kayit_basarili' isimli URL'ye yönlendir.
            return redirect('kitapkayit:kayit_basarili')
    else:
        # Sayfa ilk açıldığında boş bir form göster.
        form = KitapKayitForm()

    return render(request, 'kitapkayit/kayit_formu.html', {'form': form})

def kayit_basarili_view(request):
    # Sadece başarı mesajını gösteren basit bir view.
    return render(request, 'kitapkayit/kayit_basarili.html')
