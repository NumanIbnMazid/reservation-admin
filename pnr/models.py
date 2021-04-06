from django.db import models
from user.models import SkytripUser
from payment.models import Payment


class PNR(models.Model):
    class DataSource(models.TextChoices):
        SKYTRIP_B2C = "B2C", ("B2C")
        SKYTRIP_B2B_AGENT = "B2B_AGENT", ("B2B_AGENT")
        SKYTRIP_B2B_ADMIN = "B2B_ADMIN", ("B2B_ADMIN")
    user_id = models.CharField(
        max_length=100, verbose_name="user id"
    )
    data_source = models.CharField(
        max_length=20, choices=DataSource.choices, verbose_name="data source"
    )
    payment = models.ForeignKey(
        Payment, null=True, blank=True, on_delete=models.CASCADE, related_name="payment_pnr", verbose_name="payment"
    )
    pnr_no = models.CharField(
        max_length=23, verbose_name="pnr no"
    )
    is_production = models.BooleanField(
        verbose_name="is production"
    )
    is_ticketed = models.BooleanField(
        default=False, verbose_name="is ticketed"
    )
    # route 1
    route_1_origin_location_code = models.CharField(
        max_length=5, verbose_name="route 1 origin location code"
    )
    route_1_destination_location_code = models.CharField(
        max_length=5, verbose_name="route 1 destination location code"
    )
    route_1_departure_date = models.DateTimeField(
        verbose_name="route 1 departure date"
    )
    # route 2
    route_2_origin_location_code = models.CharField(
        max_length=5, blank=True, null=True, verbose_name="route 2 origin location code"
    )
    route_2_destination_location_code = models.CharField(
        max_length=5, blank=True, null=True, verbose_name="route 2 destination location code"
    )
    route_2_departure_date = models.DateTimeField(
        blank=True, null=True, verbose_name="route 2 departure date"
    )
    # route 3
    route_3_origin_location_code = models.CharField(
        max_length=5, blank=True, null=True, verbose_name="route 3 origin location code"
    )
    route_3_destination_location_code = models.CharField(
        max_length=5, blank=True, null=True, verbose_name="route 3 destination location code"
    )
    route_3_departure_date = models.DateTimeField(
        blank=True, null=True, verbose_name="route 3 departure date"
    )
    # route 4
    route_4_origin_location_code = models.CharField(
        max_length=5, blank=True, null=True, verbose_name="route 4 origin location code"
    )
    route_4_destination_location_code = models.CharField(
        max_length=5, blank=True, null=True, verbose_name="route 4 destination location code"
    )
    route_4_departure_date = models.DateTimeField(
        blank=True, null=True, verbose_name="route 4 departure date"
    )
    # carrier code
    carrier_code = models.CharField(
        blank=True, null=True, max_length=3, verbose_name="carrier code"
    )
    # flight number
    flight_number = models.CharField(
        blank=True, null=True, max_length=10, verbose_name="flight number"
    )
    # cabin class
    cabin_class = models.CharField(
        blank=True, null=True, max_length=23, verbose_name="cabin class"
    )
    total_amount = models.FloatField(
        null=True, blank=True, verbose_name="total amount"
    )
    currency = models.CharField(
        blank=True, null=True, max_length=7, verbose_name="currency"
    )
    utils = models.JSONField(
        null=True, blank=True, verbose_name="utils", default=dict
    )
    sabre_token = models.JSONField(
        verbose_name="sabre token", default=dict
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='created at'
    )

    class Meta:
        db_table = "pnr"
        verbose_name = ("pnr")
        verbose_name_plural = ("pnrs")
        ordering = ["-created_at"]

    def __str__(self):
        return self.pnr_no

    def get_fields(self):
        def get_dynamic_fields(field):
            if field.name == 'user':
                return (field.name, self.user.name)
            elif field.name == 'payment' and not self.payment == None:
                return (field.name, self.payment.tran_id)
            else:
                return (field.name, field.value_from_object(self))
        return [get_dynamic_fields(field) for field in self.__class__._meta.fields]
    


class PnrDetails(models.Model):
    pnr = models.ForeignKey(
        PNR, on_delete=models.CASCADE, related_name="pnr_details_pnr_id", verbose_name="pnr id"
    )
    # Passenger Personal Information
    passenger_name_number = models.CharField(
        max_length=10, verbose_name="passenger name number"
    )
    passenger_given_name = models.CharField(
        max_length=70, verbose_name="passenger given name"
    )
    passenger_surname = models.CharField(
        max_length=70, verbose_name="passenger surname"
    )
    passenger_email = models.EmailField(
        max_length=254, blank=True, null=True, verbose_name="passenger email"
    )
    passenger_contact = models.CharField(
        max_length=20, blank=True, null=True, verbose_name="passenger contact"
    )
    passenger_dob = models.DateField(
        verbose_name="passenger dob"
    )
    passenger_gender = models.CharField(
        max_length= 7, verbose_name="passenger gender"
    )
    passenger_type = models.CharField(
        max_length=23, verbose_name="passenger type"
    )
    # Passport Information
    passport_number = models.CharField(
        max_length=100, blank=True, null=True, verbose_name="passport number"
    )
    passport_issuing_country = models.CharField(
        max_length=90, blank=True, null=True, verbose_name="passport issuing country"
    )
    passport_nationality_country = models.CharField(
        max_length=90, blank=True, null=True, verbose_name="passport nationality country"
    )
    passport_expiration_date = models.DateField(
        blank=True, null=True, verbose_name="passport expiration date"
    )
    # Visa Information
    visa_number = models.CharField(
        max_length=100, blank=True, null=True, verbose_name="visa number"
    )
    visa_applicable_country = models.CharField(
        max_length=90, blank=True, null=True, verbose_name="visa applicable country"
    )
    visa_place_of_birth = models.CharField(
        max_length=255, blank=True, null=True, verbose_name="visa place of birth"
    )
    visa_place_of_issue = models.CharField(
        max_length=255, blank=True, null=True, verbose_name="visa place of issue"
    )
    visa_issue_date = models.DateField(
        blank=True, null=True, verbose_name="visa issue date"
    )
    visa_expiration_date = models.DateField(
        blank=True, null=True, verbose_name="visa expiration date"
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='created at'
    )

    class Meta:
        db_table = "pnr_details"
        verbose_name = ("pnr details")
        verbose_name_plural = ("pnr details list")
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


class PNRcarrierCodeStats(models.Model):
    carrier_code = models.CharField(
        unique=True, max_length=3, verbose_name="carrier code"
    )
    number_of_pnrs = models.IntegerField(
        default=1, verbose_name="number of pnrs"
    )
    pnr_list = models.JSONField(
        null=True, blank=True, verbose_name="pnr list", default=list
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='created at'
    )
    # updated_at = models.DateTimeField(
    #     auto_now=True, verbose_name='updated at'
    # )

    class Meta:
        db_table = "pnr_carrier_code_stats"
        verbose_name = ("pnr carrier code statistic")
        verbose_name_plural = ("pnr carrier code statistics")
        ordering = ["-created_at"]

    def __str__(self):
        return self.carrier_code
