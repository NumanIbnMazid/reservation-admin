from django.db import models
from django.conf import settings
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from util.utils import time_str_mix_slug
from middlewares.middlewares import RequestMiddleware
from django.contrib.auth.models import Group, Permission, User
from util.helpers import get_dynamic_fields

# Add Class Method to User Model


def get_groups(self):
    return "\n".join(["| " + g.name + " | " for g in self.groups.all()])


User.add_to_class("get_groups", get_groups)


# Add Class Method to Permission Model
def get_fields(self):
    return [get_dynamic_fields(field, self) for field in self.__class__._meta.fields]

Permission.add_to_class("get_fields", get_fields)


# Add Class Method to Group Model

def get_permissions(self):
    return "\n".join(["| " + p.name + " | " for p in self.permissions.all()])
    
Group.add_to_class("get_permissions", get_permissions)


# Add Class Method to Group Model
def get_fields(self):
    def get_dynamic_fields(field):
        if field.name == 'permissions':
            if field.get_internal_type() == 'ManyToManyField':
                value = ','.join([str(elem)
                                    for elem in self.permissions.all()])
            else:
                value = self.permissions.name
            return (field.name, value)
        else:
            value = "-"
            if not field.value_from_object(self) == None and not field.value_from_object(self) == "":
                value = field.value_from_object(self)
            return (field.name, value)
    return [get_dynamic_fields(field) for field in (self.__class__._meta.fields + self.__class__._meta.many_to_many)]


Group.add_to_class("get_fields", get_fields)



class Profile(models.Model):
    class Gender(models.TextChoices):
        MALE = "M", ("Male")
        FEMALE = "F", ("Female")
        OTHER = "O", ("Other")
        UNDEFINED = "U", ("Do Not Mention")

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, unique=True, related_name='user_profile', verbose_name='user'
    )
    slug = models.SlugField(
        unique=True, verbose_name='slug'
    )
    gender = models.CharField(
        max_length=10, blank=True, null=True, choices=Gender.choices, default=None, verbose_name="gender"
    )
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='profile_created_by', verbose_name="created by", blank=True, null=True
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='created at'
    )
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name='updated at'
    )

    class Meta:
        verbose_name = ("Profile")
        verbose_name_plural = ("Profiles")
        ordering = ["-user__date_joined"]

    def get_fields(self):
        def get_dynamic_fields(field):
            if field.name == 'user':
                return (field.name, self.user.username)
            else:
                return (field.name, field.value_from_object(self))
        return [get_dynamic_fields(field) for field in self.__class__._meta.fields]

    def username(self):
        return self.user.username

    def get_fullname(self):
        if self.user.first_name or self.user.last_name:
            name = self.user.get_full_name()
        else:
            name = self.user.username
        return name

    def get_smallname(self):
        if self.user.first_name or self.user.last_name:
            name = self.user.get_short_name()
        else:
            name = self.user.username
        return name

    def get_dynamic_name(self):
        if len(self.user.username) < 13:
            name = self.user.username
        else:
            name = self.get_smallname()
        return name

    def get_gender(self):
        if self.gender == "M":
            return "Male"
        elif self.gender == "F":
            return "Female"
        elif self.gender == "O":
            return "Other"
        elif self.gender == "U":
            return "Do not mention"
        else:
            return "---"

    def get_user_permissions(self):
        permissions = []
        for group in self.user.groups.all():
            for permission in group.permissions.all():
                permissions.append(permission)
        return "\n".join(["| " + p.name + " | " for p in permissions])

    def __str__(self):
        return self.user.username



@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    username = instance.username.lower()
    slug_binding = username+'-'+time_str_mix_slug()
    try:
        request = RequestMiddleware(get_response=None)
        request = request.thread_local.current_request
        gender = request.POST.get("gender")
        if gender == None:
            gender = "U"
        if created:
            Profile.objects.create(
                user=instance, gender=gender, slug=slug_binding, created_by=request.user
            )
            instance.user_profile.save()
    except AttributeError:
        try:
            if created:
                Profile.objects.create(
                    user=instance, slug=slug_binding
                )
        except Exception as E:
            raise Exception(
                f"An Exception Occured. \n Exception Type: {str(E.__class__.__name__)}. Arguments: [{str(E)}]"
            )
