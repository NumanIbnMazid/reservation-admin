from django.contrib import admin
from util.mixings import CustomModelAdminMixin
from .models import TicketIssue


class TicketIssueAdmin(CustomModelAdminMixin, admin.ModelAdmin):
    pass

    class Meta:
        model = TicketIssue


admin.site.register(TicketIssue, TicketIssueAdmin)
