from django.db import models
from pnr.models import PNR


class TicketIssue(models.Model):
    pnr = models.OneToOneField(
        PNR, on_delete=models.CASCADE, unique=True, related_name="issue_ticket_pnr", verbose_name="PNR"
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='created at'
    )

    class Meta:
        db_table = "ticket_issue"
        verbose_name = ("ticket issue")
        verbose_name_plural = ("isseued tickets")
        ordering = ["-created_at"]

    def __str__(self):
        return self.pnr.pnr_no

    def get_fields(self):
        def get_dynamic_fields(field):
            if field.name == 'pnr':
                return (field.name, self.pnr.pnr_no)
            else:
                return (field.name, field.value_from_object(self))
        return [get_dynamic_fields(field) for field in self.__class__._meta.fields]
