from django import forms
from django.contrib.auth.models import User, Group, Permission
from .models import Profile
from django.conf import settings
import re
from django.core.exceptions import ValidationError
from util.helpers import validate_chars, simple_form_widget
from django.contrib.admin.widgets import FilteredSelectMultiple


class UserGroupForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(UserGroupForm, self).__init__(*args, **kwargs)

        self.fields['name'].widget.attrs.update({
            'placeholder': 'Enter group name...',
            'maxlength': 20,
            'pattern': "^[A-Za-z- ']{1,}$"
        })
        self.fields['name'].help_text = "Only [_A-z .,'-] these characters are allowed"

        self.fields['permissions'] = forms.ModelMultipleChoiceField(
            label="Permissions", required=False, help_text="Hold down “Control”, or “Command” on a Mac, to select more than one.", queryset=Permission.objects.all()
        )

    class Meta:
        model = Group
        fields = '__all__'
        widgets = {
            'permissions': FilteredSelectMultiple("Permission", False, attrs={'rows': '2'}),
        }


class UserCreateForm(forms.Form):
    first_name = forms.CharField(
        label='First Name', max_length=50, required=False, help_text="Only [_A-z .,'-] these characters are allowed", widget=forms.TextInput(attrs={'placeholder': 'Enter first name...'})
    )
    last_name = forms.CharField(
        label='Last Name', max_length=50, required=False, help_text="Only [_A-z .,'-] these characters are allowed", widget=forms.TextInput(attrs={'placeholder': 'Enter last name...'})
    )
    GENDER_CHOICES = (
        (None, '--- Select Gender ---'),
        ("M", 'Male'),
        ("F", 'Female'),
        ("O", 'Other'),
        ("U", 'Do not mention')
    )
    gender = forms.ChoiceField(required=False, help_text='Select your Gender.', choices=GENDER_CHOICES)
    username = forms.CharField(
        label='Username', max_length=255, help_text="Only [_A-z0-9-] these characters are allowed", widget=forms.TextInput(attrs={'placeholder': 'Enter username...'})
    )
    email = forms.EmailField(
        label='Email', max_length=255, help_text="Enter valid email...", widget=forms.EmailInput(attrs={'placeholder': 'Enter email...'})
    )
    password = forms.CharField(
        label='Password', max_length=100, help_text="Enter strong password", widget=forms.PasswordInput(attrs={'placeholder': 'Enter password...'})
    )
    confirm_password = forms.CharField(
        label='Confirm Password', max_length=100, help_text="Enter password again", widget=forms.PasswordInput(attrs={'placeholder': 'Enter password again...'})
    )
    user_group = forms.ModelMultipleChoiceField(
        label="User Group", required=False, help_text='Hold down “Control”, or “Command” on a Mac, to select more than one.', queryset=Group.objects.all()
    )

    def clean_first_name(self):
        data = self.cleaned_data['first_name']
        if data is not None and data != "":
            return validate_chars(
                field_data=data, allowed_chars=r"^[_A-z .,'-]+$", max_length=30
            )
        return data

    def clean_last_name(self):
        data = self.cleaned_data['last_name']
        if data is not None and data != "":
            return validate_chars(
                field_data=data, allowed_chars=r"^[_A-z .,'-]+$", max_length=30
            )
        return data
        
    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise ValidationError("Username already exists")
        return validate_chars(
            field_data=username, allowed_chars=r"^[_A-z0-9-]+$", max_length=15
        )

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise ValidationError("Email already exists")
        return email

    def clean(self):
        form_data = self.cleaned_data
        if form_data['password'] != form_data['confirm_password']:
            self._errors["password"] = ["Password do not match"]
            del form_data['password']
        return form_data


class UserUpdateForm(forms.Form):
    def __init__(self, slug, *args, **kwargs):
        self.slug = slug
        super(UserUpdateForm, self).__init__(*args, **kwargs)

    # profile_qs = Profile.objects.filter(slug=self.slug)

    # print(slug, "XXXXXXXXX")

    first_name = forms.CharField(
        label='First Name', max_length=50, required=False, help_text="Only [_A-z .,'-] these characters are allowed", widget=forms.TextInput(attrs={'placeholder': 'Enter first name...'})
    )
    last_name = forms.CharField(
        label='Last Name', max_length=50, required=False, help_text="Only [_A-z .,'-] these characters are allowed", widget=forms.TextInput(attrs={'placeholder': 'Enter last name...'})
    )
    GENDER_CHOICES = (
        (None, '--- Select Gender ---'),
        ("M", 'Male'),
        ("F", 'Female'),
        ("O", 'Other'),
        ("U", 'Do not mention')
    )
    gender = forms.ChoiceField(required=False, help_text='Select your Gender.', choices=GENDER_CHOICES)
    username = forms.CharField(
        label='Username', max_length=255, help_text="Only [_A-z0-9-] these characters are allowed", widget=forms.TextInput(attrs={'placeholder': 'Enter username...'})
    )
    user_group = forms.ModelMultipleChoiceField(
        label="User Group", required=False, help_text='Select user group.', queryset=Group.objects.all()
    )

    def clean_first_name(self):
        data = self.cleaned_data['first_name']
        if data is not None and data != "":
            return validate_chars(
                field_data=data, allowed_chars=r"^[_A-z .,'-]+$", max_length=30
            )
        return data

    def clean_last_name(self):
        data = self.cleaned_data['last_name']
        if data is not None and data != "":
            return validate_chars(
                field_data=data, allowed_chars=r"^[_A-z .,'-]+$", max_length=30
            )
        return data
        

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['last_name', 'first_name', 'username']


# class ProfileForm(forms.ModelForm):
#     def __init__(self, *args, **kwargs):
#         # magic
#         self.user = kwargs['instance'].user
#         user_kwargs = kwargs.copy()
#         user_kwargs['instance'] = self.user
#         self.uf = UserForm(*args, **user_kwargs)
#         # magic end

#         super(ProfileForm, self).__init__(*args, **kwargs)

#         self.fields.update(self.uf.fields)
#         self.initial.update(self.uf.initial)

#         self.fields['first_name'] = forms.CharField(
#             required=False, widget=forms.TextInput(attrs={'placeholder': 'Enter your first name...'})
#         )
#         self.fields['first_name'].widget.attrs.update({
#             'id': 'profile_first_name',
#             'maxlength': 15,
#             'pattern': "^[A-Za-z.,\- ]{1,}$",
#         })
#         self.fields['last_name'] = forms.CharField(
#             required=False, widget=forms.TextInput(attrs={'placeholder': 'Enter your last name...'})
#         )
#         self.fields['last_name'].widget.attrs.update({
#             'id': 'profile_last_name',
#             'maxlength': 20,
#             'pattern': "^[A-Za-z.,\- ]{1,}$"
#         })
#         # Help Texts
#         self.fields['first_name'].help_text = "Maximum length 15 and only these 'A-Za-z.,-' characters and spaces are allowed."
#         self.fields['last_name'].help_text = "Maximum length 20 and only these 'A-Za-z.,-' characters and spaces are allowed."
#         GENDER_CHOICES = (
#             (None, '--- Select Gender ---'),
#             ("M", 'Male'),
#             ("F", 'Female'),
#             ("O", 'Other'),
#             ("U", 'Do not mention'),
#         )
#         gender = forms.ChoiceField(required=False, choices = GENDER_CHOICES)
#         self.fields['gender'].help_text = 'Enter your Gender.'

#     class Meta:
#         model = Profile
#         fields = ['gender']

#     def clean_first_name(self):
#         first_name = self.cleaned_data.get("first_name")
#         if first_name != "":
#             allowed_char = re.match(r'^[A-Za-z-., ]+$', first_name)
#             length = len(first_name)
#             if length > 15:
#                 raise forms.ValidationError("Maximum 15 characters allowed !")
#             if not allowed_char:
#                 raise forms.ValidationError(
#                     "Only 'A-Za-z.,-' these characters and spaces are allowed.")
#         return first_name

#     def clean_last_name(self):
#         last_name = self.cleaned_data.get("last_name")
#         if last_name != "":
#             allowed_char = re.match(r'^[A-Za-z-., ]+$', last_name)
#             length = len(last_name)
#             if length > 20:
#                 raise forms.ValidationError("Maximum 20 characters allowed !")
#             if not allowed_char:
#                 raise forms.ValidationError(
#                     "Only 'A-Za-z.,-' these characters and spaces are allowed."
#                 )
#         return last_name


#     def save(self, *args, **kwargs):
#         self.uf.save(*args, **kwargs)
#         return super(ProfileForm, self).save(*args, **kwargs)




class ProfileForm(forms.ModelForm):
    user_group = forms.ModelMultipleChoiceField(
        label="User Group", required=False, help_text='Select user group.', queryset=Group.objects.all()
    )
    def __init__(self, *args, **kwargs):
        # magic
        self.user = kwargs['instance'].user
        user_kwargs = kwargs.copy()
        user_kwargs['instance'] = self.user
        self.uf = UserForm(*args, **user_kwargs)
        # magic end

        super(ProfileForm, self).__init__(*args, **kwargs)

        self.fields.update(self.uf.fields)
        self.initial.update(self.uf.initial)

        self.fields['first_name'] = forms.CharField(
            required=False, widget=forms.TextInput(attrs={'placeholder': 'Enter your first name...'})
        )
        self.fields['first_name'].widget.attrs.update({
            'id': 'profile_first_name',
            'maxlength': 15,
            'pattern': "^[A-Za-z.,\- ]{1,}$",
        })
        self.fields['last_name'] = forms.CharField(
            required=False, widget=forms.TextInput(attrs={'placeholder': 'Enter your last name...'})
        )
        self.fields['last_name'].widget.attrs.update({
            'id': 'profile_last_name',
            'maxlength': 20,
            'pattern': "^[A-Za-z.,\- ]{1,}$"
        })
        # Help Texts
        self.fields['first_name'].help_text = "Maximum length 15 and only these 'A-Za-z.,-' characters and spaces are allowed."
        self.fields['last_name'].help_text = "Maximum length 20 and only these 'A-Za-z.,-' characters and spaces are allowed."
        GENDER_CHOICES = (
            (None, '--- Select Gender ---'),
            ("M", 'Male'),
            ("F", 'Female'),
            ("O", 'Other'),
            ("U", 'Do not mention'),
        )
        gender = forms.ChoiceField(required=False, choices = GENDER_CHOICES)
        self.fields['gender'].help_text = 'Enter your Gender.'

        self.fields["user_group"].initial = (
            self.user.groups.all().values_list(
                'id', flat=True
            )
        )


    class Meta:
        model = Profile
        fields = ['gender']

    def clean_first_name(self):
        first_name = self.cleaned_data.get("first_name")
        if first_name != "":
            allowed_char = re.match(r'^[A-Za-z-., ]+$', first_name)
            length = len(first_name)
            if length > 15:
                raise forms.ValidationError("Maximum 15 characters allowed !")
            if not allowed_char:
                raise forms.ValidationError(
                    "Only 'A-Za-z.,-' these characters and spaces are allowed.")
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get("last_name")
        if last_name != "":
            allowed_char = re.match(r'^[A-Za-z-., ]+$', last_name)
            length = len(last_name)
            if length > 20:
                raise forms.ValidationError("Maximum 20 characters allowed !")
            if not allowed_char:
                raise forms.ValidationError(
                    "Only 'A-Za-z.,-' these characters and spaces are allowed."
                )
        return last_name


    def save(self, *args, **kwargs):
        self.uf.save(*args, **kwargs)
        return super(ProfileForm, self).save(*args, **kwargs)
