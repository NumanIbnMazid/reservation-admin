from django import forms
from .models import VisaInformation, SSLcommerzConf, ApplicationSetting, PackageInformation, CouponSetting
import re
from django.conf import settings
from django.template.defaultfilters import filesizeformat
import os
from django.core.exceptions import ValidationError
from util.helpers import validate_chars, simple_form_widget
from ckeditor.widgets import CKEditorWidget
from django.core.files.uploadedfile import UploadedFile
from django.db.models.fields.files import ImageFieldFile


class VisaInformationManageForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(VisaInformationManageForm, self).__init__(*args, **kwargs)

        self.fields['code'].widget.attrs.update({
            'placeholder': 'Enter country code...',
            'maxlength': 5,
            'pattern': "^[A-Za-z]{1,}$"
        })
        self.fields['code'].help_text = "Only [A-z] these characters and maximum 5 characters are allowed."

        self.fields['country'].widget.attrs.update({
            'placeholder': 'Enter country name...',
            'maxlength': 100,
            'pattern': "^[_A-Za-z .,'-]{1,}$"
        })
        self.fields['country'].help_text = "Only [A-z] these characters and spaces are allowed"

        self.fields['information'].help_text = "Enter details information..."
        self.fields['information'].widget.attrs.update({
            'id': 'visa_details_input',
            'placeholder': 'Enter details information...',
            'rows': 10,
            'cols': 5,
        })

    class Meta:
        model = VisaInformation
        fields = ["code", "country", "information"]
        widgets = {
            'information': CKEditorWidget(),
        }

    def clean_code(self):
        data = self.cleaned_data['code']
        if data is not None and data != "":
            return validate_chars(
                field_data=data, allowed_chars=r"^[A-z]+$", max_length=5
            )
        return data

    def clean_country(self):
        data = self.cleaned_data['country']
        if data is not None and data != "":
            return validate_chars(
                field_data=data, allowed_chars=r"^[_A-z .,'-]+$", max_length=100
            )
        return data

    def clean_details(self):
        information = self.cleaned_data.get('information')
        if not information == None:
            length = len(information)
            if length > 70000:
                raise forms.ValidationError(
                    f"Maximum 70000 characters allowed. [currently using: {length}]"
                )
        return information


class SSLcommerzConfManageForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(SSLcommerzConfManageForm, self).__init__(*args, **kwargs)

        self.fields['store_id'].widget.attrs.update({
            'placeholder': 'Enter store id...',
            'maxlength': 100
        })
        self.fields['store_password'].widget.attrs.update({
            'placeholder': 'Enter store password...',
            'maxlength': 100
        })

    class Meta:
        model = SSLcommerzConf
        fields = ["store_id", "store_password"]

    def clean_store_id(self):
        data = self.cleaned_data['store_id']
        if data is not None and data != "":
            length = len(data)
            if length > 100:
                raise forms.ValidationError(
                    f"Maximum 100 characters allowed. [currently using: {length}]"
                )
        return data

    def clean_store_password(self):
        data = self.cleaned_data['store_password']
        if data is not None and data != "":
            length = len(data)
            if length > 100:
                raise forms.ValidationError(
                    f"Maximum 100 characters allowed. [currently using: {length}]"
                )
        return data


class ApplicationSettingManageForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ApplicationSettingManageForm, self).__init__(*args, **kwargs)

        self.fields['application_name'].widget.attrs.update({
            'placeholder': 'Enter application name...',
            'maxlength': 255
        })

        self.fields['application_domain_url'].widget.attrs.update({
            'placeholder': 'Enter application domain URL...'
        })

        self.fields['skytrip_address'].widget.attrs.update({
            'placeholder': 'Enter skytrip address...'
        })

        self.fields['facebook_app_id'].widget.attrs.update({
            'placeholder': 'Enter facebook app id...'
        })

        self.fields['google_client_id'].widget.attrs.update({
            'placeholder': 'Enter google client id...'
        })

    class Meta:
        model = ApplicationSetting
        fields = [
            "application_name", "application_domain_url", "is_production", "skytrip_address", "facebook_app_id", "google_client_id"
        ]

    def clean_application_name(self):
        data = self.cleaned_data['application_name']
        if data is not None and data != "":
            length = len(data)
            if length > 255:
                raise forms.ValidationError(
                    f"Maximum 255 characters allowed. [currently using: {length}]"
                )
        return data

    def clean_skytrip_address(self):
        data = self.cleaned_data['skytrip_address']
        if data is not None and data != "":
            length = len(data)
            if length > 255:
                raise forms.ValidationError(
                    f"Maximum 255 characters allowed. [currently using: {length}]"
                )
        return data


class PackageInformationManageForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(PackageInformationManageForm, self).__init__(*args, **kwargs)

        self.fields['package_name'].widget.attrs.update({
            'placeholder': 'Enter package name...',
            'maxlength': 255
        })

        self.fields['offer_rate'].widget.attrs.update({
            'placeholder': 'Enter offer rate...'
        })

        self.fields['num_of_days'].widget.attrs.update({
            'placeholder': 'Enter number of days...'
        })

        self.fields['amount'].widget.attrs.update({
            'placeholder': 'Enter amount...'
        })

        self.fields['cut_off_amount'].widget.attrs.update({
            'placeholder': 'Enter cut off amount...'
        })

        self.fields['image'].help_text = "Only .jpg, .jpeg, .png and .svg file format is supported and maximum file size is 2.5MB."

    class Meta:
        model = PackageInformation
        fields = ["package_name", "offer_rate", "num_of_days", "amount", "cut_off_amount", "image", "summary"]
        widgets = {
            'summary': CKEditorWidget(),
        }


    def clean_package_name(self):
        data = self.cleaned_data['package_name']
        if data is not None and data != "":
            length = len(data)
            if length > 255:
                raise forms.ValidationError(
                    f"Maximum 255 characters allowed. [currently using: {length}]"
                )
        return data

    def clean_cut_off_amount(self):
        amount = self.cleaned_data['amount']
        data = self.cleaned_data['cut_off_amount']
        if data is not None and data != "":
            if data >= amount:
                raise forms.ValidationError(
                    f"Cut off amount must be smaller than amount!"
                )
        return data

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image and isinstance(image, UploadedFile):
            file_extension = os.path.splitext(image.name)[1]
            allowed_image_types = settings.ALLOWED_IMAGE_TYPES
            content_type = image.content_type.split('/')[0]
            if not file_extension in allowed_image_types:
                raise forms.ValidationError("Only %s file formats are supported! Current image format is %s" % (
                    allowed_image_types, file_extension))
            if image.size > settings.MAX_UPLOAD_SIZE:
                raise forms.ValidationError("Please keep filesize under %s. Current filesize %s" % (
                    filesizeformat(settings.MAX_UPLOAD_SIZE), filesizeformat(image.size)))
            return image
        return None


class CouponSettingManageForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CouponSettingManageForm, self).__init__(*args, **kwargs)

        self.fields['origin_location_code'].widget.attrs.update({
            'placeholder': 'Enter origin location code...',
            'id': 'origin_location_code_input',
            'maxlength': 3,
            'pattern': "^[A-Za-z]{1,}$"
        })
        self.fields['origin_location_code'].help_text = "Only [A-z] these characters are allowed."

        self.fields['destination_location_code'].widget.attrs.update({
            'placeholder': 'Enter destination location code...',
            'id': 'destination_location_code_input',
            'maxlength': 3,
            'pattern': "^[A-Za-z]{1,}$"
        })
        self.fields['destination_location_code'].help_text = "Only [A-z] these characters are allowed."

        self.fields['code'].widget.attrs.update({
            'placeholder': 'Enter coupon code...',
            'id': 'coupon_code_input',
            'maxlength': 100,
            'pattern': "^[A-Za-z0-9]{1,}$"
        })
        self.fields['code'].help_text = "Only [A-z0-9] these characters are allowed."

        self.fields['cut_off_value'].widget.attrs.update({
            'placeholder': 'Enter cut off value...',
            'pattern': "^[0-9.]{1,}$"
        })
        self.fields['cut_off_value'].help_text = "Only [0-9.] these characters are allowed."

        self.fields['max_value'].widget.attrs.update({
            'placeholder': 'Enter max value...',
            'pattern': "^[0-9.]{1,}$"
        })
        self.fields['max_value'].help_text = "Only [0-9.] these characters are allowed."


    class Meta:
        model = CouponSetting
        fields = [
            "origin_location_code", "destination_location_code", "all_route", "code", "cut_off_value", "coupon_type", "max_value"
        ]

    def clean(self):
        data = self.cleaned_data
        origin_location_code = data.get("origin_location_code")
        destination_location_code = data.get("destination_location_code")
        all_route = data.get("all_route")
        code = data.get("code")
        cut_off_value = data.get("cut_off_value")
        coupon_type = data.get("coupon_type")
        max_value = data.get("max_value")
        # print(
        #     "Origin, Destination Location Code: ",
        #     data["origin_location_code"], data["destination_location_code"]
        # )
        # print(
        #     "All Route, Code: ", data["all_route"], data["code"]
        # )
        # print(
        #     "Cut Off Value, Coupon Type, Max Value: ", data["cut_off_value"], data["coupon_type"], data["max_value"]
        # )
        # Validation
        # --- Origin Location Code ---
        if origin_location_code is not None and origin_location_code != "":
            if origin_location_code == destination_location_code:
                self.add_error(
                    'origin_location_code', "Origin Location Code and Destination Location Code cannot be same!"
                )
        # --- Cut Off Value ---
        if cut_off_value is not None and cut_off_value != "":
            # for coupon type => fixed amount
            if max_value is not None and max_value > 0 and coupon_type == 1 and cut_off_value > max_value:
                self.add_error(
                    'cut_off_value', "For coupon type 'Fixed Amount' 'Cut Off Value' cannot be greater than 'Max Value'!"
                )
            # for coupon type => percentage
            if coupon_type == 0 and cut_off_value > 100:
                self.add_error(
                    'cut_off_value', "For coupon type 'Percenatage' 'Cut Off Value' cannot be greater than 100!"
                )
        
        # return the data
        return data

    def clean_origin_location_code(self):
        data = self.cleaned_data['origin_location_code']
        if data is not None and data != "":
            return validate_chars(
                field_data=data, allowed_chars=r"^[A-z]+$", max_length=3
            )
        return data

    def clean_destination_location_code(self):
        data = self.cleaned_data['destination_location_code']
        if data is not None and data != "":
            return validate_chars(
                field_data=data, allowed_chars=r"^[A-z]+$", max_length=3
            )
        return data

    def clean_code(self):
        data = self.cleaned_data['code']
        if data is not None and data != "":
            return validate_chars(
                field_data=data, allowed_chars=r"^[A-z0-9]+$", max_length=100
            )
        return data
