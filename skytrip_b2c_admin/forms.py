from allauth.account.forms import SignupForm
from django import forms
from django.contrib.auth.models import User


class CustomSignupForm(SignupForm):
    NONE = ''
    MALE = 'M'
    FEMALE = 'F'
    OTHER = 'O'
    UNDEFINED = 'U'
    GENDER_CHOICES = (
        (NONE, '--- Select Gender ---'),
        (MALE, 'Male'),
        (FEMALE, 'Female'),
        (OTHER, 'Other'),
        (UNDEFINED, 'Do not mention'),
    )
    gender = forms.ChoiceField(
        choices=GENDER_CHOICES, label="Gender", initial='',
         widget=forms.Select(), required=True
    )

    def signup(self, request, user):
        user.save()
        userprofile, created = self.get_or_create(user=user)
        user.userprofile.save()
