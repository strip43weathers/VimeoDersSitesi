from django.db import migrations
import os

# Bu fonksiyon, admin kullanıcısını oluşturacak
def create_superuser(apps, schema_editor):
    from django.contrib.auth import get_user_model
    User = get_user_model()

    # Ortam değişkenlerinden kullanıcı adı, e-posta ve şifreyi al
    # Render'da bu değişkenleri daha sonra ekleyeceğiz
    username = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'admin')
    email = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'admin@example.com')
    password = os.environ.get('DJANGO_SUPERUSER_PASSWORD', 'birzorsifre123')

    # Eğer bu kullanıcı adıyla bir kullanıcı yoksa oluştur
    if not User.objects.filter(username=username).exists():
        print(f"'{username}' adlı superuser oluşturuluyor...")
        User.objects.create_superuser(
            username=username,
            email=email,
            password=password
        )
    else:
        print(f"'{username}' adlı superuser zaten mevcut.")

class Migration(migrations.Migration):

    dependencies = [
        ('kullanicilar', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_superuser),
    ]
