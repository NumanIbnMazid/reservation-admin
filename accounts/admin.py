from django.contrib import admin
from django.contrib.auth.admin import UserAdmin, GroupAdmin
from util.mixings import CustomModelAdminMixin
from .models import Profile
from django.contrib.auth.models import Permission


# customize user admin
UserAdmin.list_display += ('is_active', 'id',)

# customize group admin
GroupAdmin.list_display += ('get_permissions', 'id',)


class PermissionAdmin(CustomModelAdminMixin, admin.ModelAdmin):
    pass

    class Meta:
        model = Permission

admin.site.register(Permission, PermissionAdmin)

class ProfileAdmin(CustomModelAdminMixin, admin.ModelAdmin):
    pass

    class Meta:
        model = Profile

admin.site.register(Profile, ProfileAdmin)
