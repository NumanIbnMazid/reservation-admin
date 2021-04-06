from django.contrib import admin
from util.mixings import CustomModelAdminMixin
from .models import Payment, PaymentDetails


class PaymentAdmin(CustomModelAdminMixin, admin.ModelAdmin):
    pass

    class Meta:
        model = Payment


admin.site.register(Payment, PaymentAdmin)


class PaymentDetailsAdmin(CustomModelAdminMixin, admin.ModelAdmin):
    pass

    class Meta:
        model = PaymentDetails


admin.site.register(PaymentDetails, PaymentDetailsAdmin)
