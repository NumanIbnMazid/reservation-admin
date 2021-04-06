from django.contrib import admin
from util.mixings import CustomModelAdminMixin
from .models import PNR, PnrDetails, PNRcarrierCodeStats


class PNRAdmin(CustomModelAdminMixin, admin.ModelAdmin):
    pass

    class Meta:
        model = PNR


admin.site.register(PNR, PNRAdmin)


class PnrDetailsAdmin(CustomModelAdminMixin, admin.ModelAdmin):
    pass

    class Meta:
        model = PnrDetails


admin.site.register(PnrDetails, PnrDetailsAdmin)


class PNRcarrierCodeStatsAdmin(CustomModelAdminMixin, admin.ModelAdmin):
    pass

    class Meta:
        model = PNRcarrierCodeStats


admin.site.register(PNRcarrierCodeStats, PNRcarrierCodeStatsAdmin)
