from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Profil


class ProfilInline(admin.StackedInline):
    model = Profil
    can_delete = False
    verbose_name_plural = 'Profiller'


class UserAdmin(BaseUserAdmin):
    inlines = (ProfilInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'get_onay_durumu')

    actions = ['approve_users', 'disapprove_users']

    @admin.action(description='Seçili kullanıcıları onayla')
    def approve_users(self, request, queryset):
        for user in queryset:
            user.profil.onaylandi = True
            user.profil.save()
        self.message_user(request, f"{queryset.count()} kullanıcı başarıyla onaylandı.")

    @admin.action(description='Seçili kullanıcıların onayını kaldır')
    def disapprove_users(self, request, queryset):
        for user in queryset:
            user.profil.onaylandi = False
            user.profil.save()
        self.message_user(request, f"{queryset.count()} kullanıcının onayı kaldırıldı.")

    @admin.display(description='Onay Durumu', boolean=True)
    def get_onay_durumu(self, obj):
        try:
            return obj.profil.onaylandi
        except Profil.DoesNotExist:
            return False


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
