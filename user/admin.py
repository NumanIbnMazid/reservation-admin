from django.contrib import admin
from util.mixings import CustomModelAdminMixin
from .models import SkytripUser, UserMedia


class SkytripUserAdmin(CustomModelAdminMixin, admin.ModelAdmin):
    pass

    class Meta:
        model = SkytripUser


class UserMediaAdmin(CustomModelAdminMixin, admin.ModelAdmin):
    pass

    class Meta:
        model = SkytripUser


admin.site.register(SkytripUser, SkytripUserAdmin)
admin.site.register(UserMedia, UserMediaAdmin)


admin.site.site_header = "Skytrip Admin"
admin.site.site_title = "Skytrip Admin"
