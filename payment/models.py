from django.db import models

class Payment(models.Model):
    user_email = models.EmailField(
        verbose_name="user email"
    )
    tran_id = models.CharField(
        max_length=255, verbose_name="transaction id"
    )
    transaction_log = models.TextField(
        null=True, blank=True, verbose_name="transaction log"
    )
    total_amt = models.FloatField(
        verbose_name="total amount"
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='created at'
    )

    class Meta:
        db_table = "payment"
        verbose_name = ("payment")
        verbose_name_plural = ("payments")
        ordering = ["-created_at"]

    def __str__(self):
        return self.tran_id

    def get_fields(self):
        def get_dynamic_fields(field):
            return (field.name, field.value_from_object(self))
        return [get_dynamic_fields(field) for field in self.__class__._meta.fields]


class PaymentDetails(models.Model):
    payment = models.ForeignKey(
        Payment, on_delete=models.CASCADE, related_name="payment_details_payment_id", verbose_name="payment_id"
    )
    amount = models.FloatField(
        null=True, blank=True, verbose_name="amount"
    )
    card_type = models.CharField(
        null=True, blank=True, max_length=50, verbose_name="card type"
    )
    store_amount = models.FloatField(
        null=True, blank=True, verbose_name="store amount"
    )
    card_no = models.CharField(
        null=True, blank=True, max_length=80, verbose_name="card no"
    )
    bank_tran_id = models.CharField(
        null=True, blank=True, max_length=80, verbose_name="bank transaction id"
    )
    status = models.CharField(
        null=True, blank=True, max_length=20, verbose_name="status"
    )
    tran_date = models.DateTimeField(
        null=True, blank=True, auto_now_add=True, verbose_name="transaction date"
    )
    currency = models.CharField(
        null=True, blank=True, max_length=3, verbose_name="currency"
    )
    card_issuer = models.CharField(
        max_length=50, blank=True, null=True, verbose_name="card issuer"
    )
    card_brand = models.CharField(
        max_length=30, blank=True, null=True, verbose_name="card brand"
    )
    card_issuer_country = models.CharField(
        max_length=50, blank=True, null=True, verbose_name="card issuer country"
    )
    card_issuer_country_code = models.CharField(
        max_length=50, blank=True, null=True, verbose_name="card issuer country code"
    )
    store_id = models.CharField(
        max_length=50, blank=True, null=True, verbose_name="store id"
    )
    verify_sign = models.CharField(
        max_length=255, blank=True, null=True, verbose_name="verify sign"
    )
    verify_key = models.TextField(
        blank=True, null=True, verbose_name="verify key"
    )
    cus_fax = models.CharField(
        max_length=50, blank=True, null=True, verbose_name="cus fax"
    )
    currency_type = models.CharField(
        null=True, blank=True, max_length=50, verbose_name="currency type"
    )
    currency_amount = models.FloatField(
        blank=True, null=True, verbose_name="currency amount"
    )
    currency_rate = models.FloatField(
        blank=True, null=True, verbose_name="currency rate"
    )
    base_fair = models.FloatField(
        blank=True, null=True, verbose_name="base fair"
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='created at'
    )

    class Meta:
        db_table = "payment_details"
        verbose_name = ("payment details")
        verbose_name_plural = ("payment details list")
        ordering = ["-created_at"]

    def __str__(self):
        return self.payment.tran_id

    def get_fields(self):
        def get_dynamic_fields(field):
            if field.name == 'payment':
                return (field.name, self.payment.tran_id)
            else:
                return (field.name, field.value_from_object(self))
        return [get_dynamic_fields(field) for field in self.__class__._meta.fields]
    
