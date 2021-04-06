from django.db import models

class SkytripUser(models.Model):
    user_id = models.CharField(
        max_length=100, verbose_name="user id"
    )
    name = models.CharField(
        max_length=70, verbose_name="name"
    )
    email = models.EmailField(
        max_length=254, verbose_name="email"
    )
    phone = models.CharField(
        max_length=20, blank=True, null=True, verbose_name="phone"
    )
    password = models.CharField(
        max_length=128, verbose_name="password"
    )
    ip_address = models.CharField(
        max_length=100, blank=True, null=True, verbose_name="ip address"
    )
    mac_address = models.CharField(
        max_length=20, blank=True, null=True, verbose_name="mac address"
    )
    fb_token = models.TextField(
        blank=True, null=True, verbose_name="facebook token"
    )
    google_token = models.TextField(
        blank=True, null=True, verbose_name="google token"
    )
    user_status = models.SmallIntegerField(
        blank=True, null=True, verbose_name="user status"
    )
    user_level = models.IntegerField(
        blank=True, null=True, verbose_name="user level"
    )
    login_with = models.SmallIntegerField(
        blank=True, null=True, verbose_name="login with"
    )
    date_joined = models.DateTimeField(
        auto_now_add=True, verbose_name='date joined'
    )
    last_login = models.DateTimeField(
        auto_now=True, verbose_name='last login'
    )

    class Meta:
        db_table = "skytrip_user"
        verbose_name = ("skytrip user")
        verbose_name_plural = ("skytrip users")
        ordering = ["-date_joined"]

    def __str__(self):
        return self.name

    def get_fields(self):
        def get_dynamic_fields(field):
            return (field.name, field.value_from_object(self))
        return [get_dynamic_fields(field) for field in self.__class__._meta.fields]


class UserMedia(models.Model):
    user = models.ForeignKey(
        SkytripUser, on_delete=models.CASCADE, related_name="user_skytrip_user", verbose_name="user"
    )
    media_category = models.CharField(
        max_length=100, verbose_name="media category"
    )
    media_s3_url = models.URLField(
        verbose_name="media s3 URL"
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='created at'
    )

    class Meta:
        db_table = "user_media"
        verbose_name = ("user media")
        verbose_name_plural = ("user medias")
        ordering = ["-created_at"]

    def __str__(self):
        return self.user.name

    def get_fields(self):
        def get_dynamic_fields(field):
            if field.name == 'user':
                return (field.name, self.user.name)
            else:
                return (field.name, field.value_from_object(self))
        return [get_dynamic_fields(field) for field in self.__class__._meta.fields]
