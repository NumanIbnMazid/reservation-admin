from django.contrib import admin
from util.mixings import CustomModelAdminMixin
from .models import VisaInformation, SSLcommerzConf, ApplicationSetting, PackageInformation, CouponSetting


class VisaInformationAdmin(CustomModelAdminMixin, admin.ModelAdmin):
    pass

    class Meta:
        model = VisaInformation


admin.site.register(VisaInformation, VisaInformationAdmin)


class SSLcommerzConfAdmin(CustomModelAdminMixin, admin.ModelAdmin):
    pass

    class Meta:
        model = SSLcommerzConf


admin.site.register(SSLcommerzConf, SSLcommerzConfAdmin)


class ApplicationSettingAdmin(CustomModelAdminMixin, admin.ModelAdmin):
    pass

    class Meta:
        model = ApplicationSetting


admin.site.register(ApplicationSetting, ApplicationSettingAdmin)


class PackageInformationAdmin(CustomModelAdminMixin, admin.ModelAdmin):
    pass

    class Meta:
        model = PackageInformation


admin.site.register(PackageInformation, PackageInformationAdmin)


class CouponSettingAdmin(CustomModelAdminMixin, admin.ModelAdmin):
    pass

    class Meta:
        model = CouponSetting


admin.site.register(CouponSetting, CouponSettingAdmin)
