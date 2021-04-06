from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from middlewares.middlewares import RequestMiddleware
from django.core.validators import MinValueValidator
from decimal import Decimal
from util.utils import upload_package_image_path
import os
from django.conf import settings


# # -------------------------------------------------------------------
# #                           VisaInformation
# # -------------------------------------------------------------------

class VisaInformation(models.Model):
    code = models.CharField(
        max_length=5, verbose_name="code"
    )
    country = models.CharField(
        max_length=100, verbose_name="country"
    )
    information = models.TextField(
        blank=True, null=True, verbose_name="information"
    )
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="visa_information_created_by", verbose_name="created by"
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='created at'
    )
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name='updated at'
    )

    class Meta:
        verbose_name = ("Visa Information")
        verbose_name_plural = ("Visa Information")
        ordering = ["-created_at"]

    def __str__(self):
        return self.country

    def get_fields(self):
        def get_dynamic_fields(field):
            if field.name == 'created_by':
                return (field.name, self.created_by.username)
            else:
                return (field.name, field.value_from_object(self))
        return [get_dynamic_fields(field) for field in self.__class__._meta.fields]


# # -------------------------------------------------------------------
# #                           SSLcommerzConf
# # -------------------------------------------------------------------


class SSLcommerzConf(models.Model):
    store_id = models.CharField(
        max_length=100, verbose_name="store id"
    )
    store_password = models.CharField(
        max_length=100, verbose_name="store password"
    )
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="ssl_commerz_conf_created_by", verbose_name="created by"
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='created at'
    )
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name='updated at'
    )

    class Meta:
        verbose_name = ("SSL Commerz Conf")
        verbose_name_plural = ("SSL Commerz Confs")
        ordering = ["-created_at"]

    def __str__(self):
        return self.store_id

    def get_fields(self):
        def get_dynamic_fields(field):
            if field.name == 'created_by':
                return (field.name, self.created_by.username)
            else:
                return (field.name, field.value_from_object(self))
        return [get_dynamic_fields(field) for field in self.__class__._meta.fields]


# # -------------------------------------------------------------------
# #                           ApplicationSetting
# # -------------------------------------------------------------------

class ApplicationSetting(models.Model):
    application_name = models.CharField(
        max_length=255, verbose_name="application name"
    )
    application_domain_url = models.URLField(
        verbose_name="application domain url"
    )
    is_production = models.BooleanField(
        default=False, verbose_name="is prodcution"
    )
    skytrip_address = models.CharField(
        max_length=255, blank=True, null=True, verbose_name="skytrip address"
    )
    facebook_app_id = models.CharField(
        max_length=100, blank=True, null=True, verbose_name="facebook app id"
    )
    google_client_id = models.CharField(
        max_length=255, blank=True, null=True, verbose_name="google client id"
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='created at'
    )
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name='updated at'
    )

    class Meta:
        verbose_name = ("Application Setting")
        verbose_name_plural = ("Application Settings")
        ordering = ["-created_at"]

    def __str__(self):
        return self.application_name

    def get_fields(self):
        def get_dynamic_fields(field):
            return (field.name, field.value_from_object(self))
        return [get_dynamic_fields(field) for field in self.__class__._meta.fields]


# # -------------------------------------------------------------------
# #                           PackageInformation
# # -------------------------------------------------------------------

class PackageInformation(models.Model):
    package_name = models.CharField(
        max_length=255, verbose_name="package name"
    )
    offer_rate = models.DecimalField(
        decimal_places=2, max_digits=10, validators=[MinValueValidator(
            Decimal(0.00)
        )], null=True, blank=True, verbose_name='offer rate'
    )
    num_of_days = models.SmallIntegerField(
        null=True, blank=True,  verbose_name="num of days"
    )
    amount = models.DecimalField(
        decimal_places=2, max_digits=10, validators=[MinValueValidator(
            Decimal(0.00)
        )], null=True, blank=True, verbose_name='amount'
    )
    cut_off_amount = models.DecimalField(
        decimal_places=2, max_digits=10, validators=[MinValueValidator(
            Decimal(0.00)
        )], null=True, blank=True, verbose_name='cut off amount'
    )
    image = models.ImageField(
        upload_to=upload_package_image_path, verbose_name="image"
    )
    summary = models.TextField(
        blank=True, null=True, verbose_name="summary"
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='created at'
    )
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name='updated at'
    )

    class Meta:
        verbose_name = ("Package Information")
        verbose_name_plural = ("Package Information")
        ordering = ["-created_at"]

    def __str__(self):
        return self.package_name

    def get_fields(self):
        def get_dynamic_fields(field):
            # if field.name == "image":
            #     return (field.name, settings.S3_MEDIA_OBJECT_URL + field.value_from_object(self).url)
            return (field.name, field.value_from_object(self))
        return [get_dynamic_fields(field) for field in self.__class__._meta.fields]


# # -------------------------------------------------------------------
# #                           CouponSetting
# # -------------------------------------------------------------------

class CouponSetting(models.Model):
    class CouponTypeChoice(models.IntegerChoices):
        PERCENTAGE = 0, ("Percentage")
        FIXED = 1, ("Fixed Amount")
    origin_location_code = models.CharField(
        max_length=7, blank=True, null=True, verbose_name="origin location code"
    )
    destination_location_code = models.CharField(
        max_length=7, blank=True, null=True, verbose_name="destination location code"
    )
    all_route = models.BooleanField(
        default=False, verbose_name="for all routes"
    )
    code = models.CharField(
        max_length=255, unique=True, verbose_name="coupon code"
    )
    cut_off_value = models.DecimalField(
        decimal_places=2, max_digits=10, validators=[MinValueValidator(
            Decimal(0.00)
        )], verbose_name='cut off value'
    )
    coupon_type = models.SmallIntegerField(
        choices=CouponTypeChoice.choices, default=0, verbose_name="coupon type"
    )
    max_value = models.DecimalField(
        decimal_places=2, max_digits=10, validators=[MinValueValidator(
            Decimal(0.00)
        )], default=0, null=True, blank=True, verbose_name='max value'
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='created at'
    )
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name='updated at'
    )

    class Meta:
        verbose_name = ("Coupon Setting")
        verbose_name_plural = ("Coupon Settings")
        ordering = ["-created_at"]

    def __str__(self):
        return self.code

    def get_fields(self):
        def get_dynamic_fields(field):
            return (field.name, field.value_from_object(self))
        return [get_dynamic_fields(field) for field in self.__class__._meta.fields]




# Pre Save Receiver for SSLcommerzConf
def update_ssl_commerz_conf_created_by(sender, instance, *args, **kwargs):
    # if not instance.created_by:
    try:
        request = RequestMiddleware(get_response=None)
        request = request.thread_local.current_request
        instance.created_by = request.user
    except Exception as E:
        raise Exception(
            f"An Exception Occured. Failed to update SSLcommerzConf 'created_by' \n Exception Type: {str(E.__class__.__name__)}. Arguments: [{str(E)}]"
        )


pre_save.connect(update_ssl_commerz_conf_created_by, sender=SSLcommerzConf)


# Pre Save Reciever for VisaInformation
def update_visa_information_created_by(sender, instance, *args, **kwargs):
    # if not instance.created_by:
    try:
        request = RequestMiddleware(get_response=None)
        request = request.thread_local.current_request
        instance.created_by = request.user
    except Exception as E:
        raise Exception(
            f"An Exception Occured. Failed to update VisaInformation 'created_by' \n Exception Type: {str(E.__class__.__name__)}. Arguments: [{str(E)}]"
        )


pre_save.connect(update_visa_information_created_by, sender=VisaInformation)
