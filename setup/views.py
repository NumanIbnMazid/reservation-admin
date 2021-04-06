from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from django.views.generic import CreateView, UpdateView, DetailView, TemplateView
from .forms import (
    VisaInformationManageForm, SSLcommerzConfManageForm, ApplicationSettingManageForm, PackageInformationManageForm, CouponSettingManageForm
)
from .models import (
    VisaInformation, SSLcommerzConf, ApplicationSetting, PackageInformation, CouponSetting
)
from django.contrib import messages
from django import forms
from util.helpers import (
    validate_normal_form, simple_context_data, get_simple_object, delete_simple_object, user_has_permission
)
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
# Custom Decorators Starts
from util.decorators import (
    has_permission_required
)
# Custom Decorators Ends

# # -------------------------------------------------------------------
# #                           VisaInformation
# # -------------------------------------------------------------------

class VisaInformationCreateView(CreateView):
    template_name = "setup/visa-information-manage.html"
    form_class = VisaInformationManageForm

    def form_valid(self, form):
        code = form.instance.code
        field_qs = VisaInformation.objects.filter(
            code__iexact=code
        )
        result = validate_normal_form(
            field='code', field_qs=field_qs,
            form=form, request=self.request
        )
        if result == 1:
            return super().form_valid(form)
        else:
            return super().form_invalid(form)

    def get_success_url(self):
        return reverse('setup:create_visa_information')

    def get_context_data(self, **kwargs):
        context = super(
            VisaInformationCreateView, self
        ).get_context_data(**kwargs)
        context['page_title'] = 'Create Visa Information'
        context['page_short_title'] = 'Create Visa Information'
        context['list_objects'] = VisaInformation.objects.all().order_by('-id')
        context['list_template'] = "setup/visa-information-datatable.html"
        context['fields_count'] = len(VisaInformation._meta.get_fields()) + 1
        context['fields'] = dict([(f.name, f.verbose_name)
                                  for f in VisaInformation._meta.fields + VisaInformation._meta.many_to_many])
        context["update_url"] = "setup:update_visa_information"
        context["delete_url"] = "setup:delete_visa_information"
        context["detail_url"] = "setup:visa_information_detail"
        context['namespace'] = 'visa_information'
        context['can_add_change'] = True if self.request.user.has_perm(
            'setup.add_visainformation') and self.request.user.has_perm('setup.change_visainformation') else False
        context['can_view'] = self.request.user.has_perm(
            'setup.view_visainformation')
        context['can_delete'] = self.request.user.has_perm(
            'setup.delete_visainformation')
        return context

class VisaInformationUpdateView(UpdateView):
    template_name = "setup/visa-information-manage.html"
    form_class = VisaInformationManageForm

    def get_object(self):
        return get_simple_object(key="id", model=VisaInformation, self=self)

    def form_valid(self, form):
        code = form.instance.code
        self.object = self.get_object()
        if not self.object.code == code:
            field_qs = VisaInformation.objects.filter(
                code__iexact=code
            )
            result = validate_normal_form(
                field='code', field_qs=field_qs,
                form=form, request=self.request
            )
            if result == 1:
                return super().form_valid(form)
            else:
                return super().form_invalid(form)
        messages.add_message(
            self.request, messages.SUCCESS, "Visa Information Updated Successfully!"
        )
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('setup:create_visa_information')

    def get_context_data(self, **kwargs):
        context = super(
            VisaInformationUpdateView, self
        ).get_context_data(**kwargs)
        context['page_title'] = f'Update {self.get_object().code} Visa Information'
        context['page_short_title'] = f'Update {self.get_object().code} Visa Information'
        context['list_objects'] = VisaInformation.objects.all().order_by('-id')
        context['list_template'] = "setup/visa-information-datatable.html"
        context['fields_count'] = len(VisaInformation._meta.get_fields()) + 1
        context['fields'] = dict([(f.name, f.verbose_name)
                                  for f in VisaInformation._meta.fields + VisaInformation._meta.many_to_many])
        context["update_url"] = "setup:update_visa_information"
        context["delete_url"] = "setup:delete_visa_information"
        context["detail_url"] = "setup:visa_information_detail"
        context['namespace'] = 'visa_information'
        context['can_add_change'] = True if self.request.user.has_perm(
            'setup.add_visainformation') and self.request.user.has_perm('setup.change_visainformation') else False
        context['can_view'] = self.request.user.has_perm(
            'setup.view_visainformation')
        context['can_delete'] = self.request.user.has_perm(
            'setup.delete_visainformation')
        return context


class VisaInformationDetailView(DetailView):
    template_name = "setup/visa-information-detail.html"

    def get_object(self):
        return get_simple_object(key='id', model=VisaInformation, self=self)

    def get_context_data(self, **kwargs):
        context = super(
            VisaInformationDetailView, self
        ).get_context_data(**kwargs)
        context['page_title'] = f'{self.get_object().code} - Visa Information Detail'
        context['page_short_title'] = f'{self.get_object().code} - Visa Information Detail'
        context["create_url"] = "setup:create_visa_information"
        context["update_url"] = "setup:update_visa_information"
        context["delete_url"] = "setup:delete_visa_information"
        context["list_url"] = "setup:create_visa_information"
        context['can_add_change'] = True if self.request.user.has_perm(
            'setup.add_visainformation') and self.request.user.has_perm('setup.change_visainformation') else False
        context['can_view'] = self.request.user.has_perm(
            'setup.view_visainformation')
        context['can_delete'] = self.request.user.has_perm(
            'setup.delete_visainformation')
        return context


@csrf_exempt
def delete_visa_information(request):
    return delete_simple_object(request=request, key='id', model=VisaInformation, redirect_url="setup:create_visa_information")


# # -------------------------------------------------------------------
# #                           SSLcommerzConf
# # -------------------------------------------------------------------

class SSLcommerzConfCreateView(CreateView):
    template_name = "snippets/manage.html"
    form_class = SSLcommerzConfManageForm

    def form_valid(self, form):
        store_id = form.instance.store_id
        field_qs = SSLcommerzConf.objects.filter(
            store_id__iexact=store_id
        )
        result = validate_normal_form(
            field='store_id', field_qs=field_qs,
            form=form, request=self.request
        )
        if result == 1:
            return super().form_valid(form)
        else:
            return super().form_invalid(form)

    def get_success_url(self):
        return reverse('setup:create_ssl_commerz_conf')

    def get_context_data(self, **kwargs):
        context = super(
            SSLcommerzConfCreateView, self
        ).get_context_data(**kwargs)
        context['page_title'] = 'Create SSL Commerz Conf'
        context['page_short_title'] = 'Create SSL Commerz Conf'
        context['list_objects'] = SSLcommerzConf.objects.all().order_by('-id')
        context['list_template'] = None
        context['fields_count'] = len(SSLcommerzConf._meta.get_fields()) + 1
        context['fields'] = dict([(f.name, f.verbose_name)
                                  for f in SSLcommerzConf._meta.fields + SSLcommerzConf._meta.many_to_many])
        context["update_url"] = "setup:update_ssl_commerz_conf"
        context["delete_url"] = "setup:delete_ssl_commerz_conf"
        context["detail_url"] = "setup:ssl_commerz_conf_detail"
        context['namespace'] = 'ssl_commerz_conf'
        context['can_add_change'] = True if self.request.user.has_perm(
            'setup.add_sslcommerzconf') and self.request.user.has_perm('setup.change_sslcommerzconf') else False
        context['can_view'] = self.request.user.has_perm(
            'setup.view_sslcommerzconf')
        context['can_delete'] = self.request.user.has_perm(
            'setup.delete_sslcommerzconf')
        return context

class SSLcommerzConfUpdateView(UpdateView):
    template_name = "snippets/manage.html"
    form_class = SSLcommerzConfManageForm

    def get_object(self):
        return get_simple_object(key="id", model=SSLcommerzConf, self=self)

    def form_valid(self, form):
        store_id = form.instance.store_id
        self.object = self.get_object()
        if not self.object.store_id == store_id:
            field_qs = SSLcommerzConf.objects.filter(
                store_id__iexact=store_id
            )
            result = validate_normal_form(
                field='store_id', field_qs=field_qs,
                form=form, request=self.request
            )
            if result == 1:
                return super().form_valid(form)
            else:
                return super().form_invalid(form)
        messages.add_message(
            self.request, messages.SUCCESS, "SSL Commerz Conf Updated Successfully!"
        )
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('setup:create_ssl_commerz_conf')

    def get_context_data(self, **kwargs):
        context = super(
            SSLcommerzConfUpdateView, self
        ).get_context_data(**kwargs)
        context['page_title'] = f'Update {self.get_object().store_id} SSL Commerz Conf'
        context['page_short_title'] = f'Update {self.get_object().store_id} SSL Commerz Conf'
        context['list_objects'] = SSLcommerzConf.objects.all().order_by('-id')
        context['list_template'] = None
        context['fields_count'] = len(SSLcommerzConf._meta.get_fields()) + 1
        context['fields'] = dict([(f.name, f.verbose_name)
                                  for f in SSLcommerzConf._meta.fields + SSLcommerzConf._meta.many_to_many])
        context["update_url"] = "setup:update_ssl_commerz_conf"
        context["delete_url"] = "setup:delete_ssl_commerz_conf"
        context["detail_url"] = "setup:ssl_commerz_conf_detail"
        context['namespace'] = 'ssl_commerz_conf'
        context['can_add_change'] = True if self.request.user.has_perm(
            'setup.add_sslcommerzconf') and self.request.user.has_perm('setup.change_sslcommerzconf') else False
        context['can_view'] = self.request.user.has_perm(
            'setup.view_sslcommerzconf')
        context['can_delete'] = self.request.user.has_perm(
            'setup.delete_sslcommerzconf')
        return context


class SSLcommerzConfDetailView(DetailView):
    template_name = "snippets/detail-common.html"

    def get_object(self):
        return get_simple_object(key='id', model=SSLcommerzConf, self=self)

    def get_context_data(self, **kwargs):
        context = super(
            SSLcommerzConfDetailView, self
        ).get_context_data(**kwargs)
        context['page_title'] = f'{self.get_object().store_id} - SSL Commerz Conf Detail'
        context['page_short_title'] = f'{self.get_object().store_id} - SSL Commerz Conf Detail'
        context["create_url"] = "setup:create_ssl_commerz_conf"
        context["update_url"] = "setup:update_ssl_commerz_conf"
        context["delete_url"] = "setup:delete_ssl_commerz_conf"
        context["list_url"] = "setup:create_ssl_commerz_conf"
        context['can_add_change'] = True if self.request.user.has_perm(
            'setup.add_sslcommerzconf') and self.request.user.has_perm('setup.change_sslcommerzconf') else False
        context['can_view'] = self.request.user.has_perm(
            'setup.view_sslcommerzconf')
        context['can_delete'] = self.request.user.has_perm(
            'setup.delete_sslcommerzconf')
        return context


@csrf_exempt
def delete_ssl_commerz_conf(request):
    return delete_simple_object(request=request, key='id', model=SSLcommerzConf, redirect_url="setup:create_ssl_commerz_conf")


# # -------------------------------------------------------------------
# #                           Application Setting
# # -------------------------------------------------------------------

class ApplicationSettingUpdateView(UpdateView):
    template_name = "snippets/manage.html"
    form_class = ApplicationSettingManageForm

    def get_object(self):
        qs = ApplicationSetting.objects.all()
        if qs.exists():
            return qs.first()
        return None

    def form_valid(self, form):
        messages.add_message(
            self.request, messages.SUCCESS, "Application Settings Updated Successfully!"
        )
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('setup:update_application_setting', kwargs={"id":"skytrip"})

    def get_context_data(self, **kwargs):
        context = super(
            ApplicationSettingUpdateView, self
        ).get_context_data(**kwargs)
        context['page_title'] = f'Update Application Setting'
        context['page_short_title'] = f'Update Application Setting'
        context['list_objects'] = ApplicationSetting.objects.all().order_by('-id')
        context['list_template'] = None
        context['fields_count'] = len(ApplicationSetting._meta.get_fields()) + 1
        context['fields'] = dict([(f.name, f.verbose_name)
                                  for f in ApplicationSetting._meta.fields + ApplicationSetting._meta.many_to_many])
        context["update_url"] = "setup:update_application_setting"
        context["delete_url"] = None
        context["detail_url"] = "setup:application_setting_detail"
        context['namespace'] = 'application_setting'
        context['can_add_change'] = True if self.request.user.has_perm(
            'setup.add_applicationsetting') and self.request.user.has_perm('setup.change_applicationsetting') else False
        context['can_view'] = self.request.user.has_perm(
            'setup.view_applicationsetting')
        context['can_delete'] = self.request.user.has_perm(
            'setup.delete_applicationsetting')
        return context


class ApplicationSettingDetailView(DetailView):
    template_name = "snippets/detail-common.html"

    def get_object(self):
        qs = ApplicationSetting.objects.all()
        if qs.exists():
            return qs.first()
        return None

    def get_context_data(self, **kwargs):
        context = super(
            ApplicationSettingDetailView, self
        ).get_context_data(**kwargs)
        context['page_title'] = f'Update Application Setting'
        context['page_short_title'] = f'Update Application Setting'
        context["create_url"] = None
        context["update_url"] = "setup:update_application_setting"
        context["delete_url"] = None
        context["list_url"] = None
        context['can_add_change'] = True if self.request.user.has_perm(
            'setup.add_applicationsetting') and self.request.user.has_perm('setup.change_applicationsetting') else False
        context['can_view'] = self.request.user.has_perm(
            'setup.view_applicationsetting')
        context['can_delete'] = self.request.user.has_perm(
            'setup.delete_applicationsetting')
        return context


# # -------------------------------------------------------------------
# #                           PackageInformation
# # -------------------------------------------------------------------

class PackageInformationCreateView(CreateView):
    template_name = "setup/package-information/manage.html"
    form_class = PackageInformationManageForm

    def form_valid(self, form):
        package_name = form.instance.package_name
        image = form.instance.image
        field_qs = PackageInformation.objects.filter(
            package_name__iexact=package_name
        )
        result = validate_normal_form(
            field='package_name', field_qs=field_qs,
            form=form, request=self.request
        )
        if result == 1:
            return super().form_valid(form)
        else:
            return super().form_invalid(form)

    def get_success_url(self):
        return reverse('setup:create_package_information')

    def get_context_data(self, **kwargs):
        context = super(
            PackageInformationCreateView, self
        ).get_context_data(**kwargs)
        context['page_title'] = 'Create Package Information'
        context['page_short_title'] = 'Create Package Information'
        context['list_objects'] = PackageInformation.objects.all().order_by('-id')
        context['list_template'] = None
        context['fields_count'] = len(PackageInformation._meta.get_fields()) + 1
        context['fields'] = dict([(f.name, f.verbose_name)
                                  for f in PackageInformation._meta.fields + PackageInformation._meta.many_to_many])
        context["update_url"] = "setup:update_package_information"
        context["delete_url"] = "setup:delete_package_information"
        context["detail_url"] = "setup:package_information_detail"
        context['namespace'] = 'package_information'
        context['can_add_change'] = True if self.request.user.has_perm(
            'setup.add_packageinformation') and self.request.user.has_perm('setup.change_packageinformation') else False
        context['can_view'] = self.request.user.has_perm(
            'setup.view_packageinformation')
        context['can_delete'] = self.request.user.has_perm(
            'setup.delete_packageinformation')
        return context


class PackageInformationUpdateView(UpdateView):
    template_name = "setup/package-information/manage.html"
    form_class = PackageInformationManageForm

    def get_object(self):
        return get_simple_object(key="id", model=PackageInformation, self=self)

    def form_valid(self, form):
        package_name = form.instance.package_name
        self.object = self.get_object()
        if not self.object.package_name == package_name:
            field_qs = PackageInformation.objects.filter(
                package_name__iexact=package_name
            )
            result = validate_normal_form(
                field='package_name', field_qs=field_qs,
                form=form, request=self.request
            )
            if result == 1:
                return super().form_valid(form)
            else:
                return super().form_invalid(form)
        messages.add_message(
            self.request, messages.SUCCESS, "Package Information Updated Successfully!"
        )
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('setup:create_package_information')

    def get_context_data(self, **kwargs):
        context = super(
            PackageInformationUpdateView, self
        ).get_context_data(**kwargs)
        context['page_title'] = f'Update {self.get_object().package_name} Package Information'
        context['page_short_title'] = f'Update {self.get_object().package_name} Package Information'
        context['list_objects'] = PackageInformation.objects.all().order_by('-id')
        context['list_template'] = None
        context['fields_count'] = len(PackageInformation._meta.get_fields()) + 1
        context['fields'] = dict([(f.name, f.verbose_name)
                                  for f in PackageInformation._meta.fields + PackageInformation._meta.many_to_many])
        context["update_url"] = "setup:update_package_information"
        context["delete_url"] = "setup:delete_package_information"
        context["detail_url"] = "setup:package_information_detail"
        context['namespace'] = 'package_information'
        context['can_add_change'] = True if self.request.user.has_perm(
            'setup.add_packageinformation') and self.request.user.has_perm('setup.change_packageinformation') else False
        context['can_view'] = self.request.user.has_perm(
            'setup.view_packageinformation')
        context['can_delete'] = self.request.user.has_perm(
            'setup.delete_packageinformation')
        return context


class PackageInformationDetailView(DetailView):
    template_name = "setup/package-information/detail.html"

    def get_object(self):
        return get_simple_object(key='id', model=PackageInformation, self=self)

    def get_context_data(self, **kwargs):
        context = super(
            PackageInformationDetailView, self
        ).get_context_data(**kwargs)
        context['page_title'] = f'{self.get_object().package_name} - package Information Detail'
        context['page_short_title'] = f'{self.get_object().package_name} - package Information Detail'
        context["create_url"] = "setup:create_package_information"
        context["update_url"] = "setup:update_package_information"
        context["delete_url"] = "setup:delete_package_information"
        context["list_url"] = "setup:create_package_information"
        context['can_add_change'] = True if self.request.user.has_perm(
            'setup.add_packageinformation') and self.request.user.has_perm('setup.change_packageinformation') else False
        context['can_view'] = self.request.user.has_perm(
            'setup.view_packageinformation')
        context['can_delete'] = self.request.user.has_perm(
            'setup.delete_packageinformation')
        return context


@csrf_exempt
def delete_package_information(request):
    return delete_simple_object(request=request, key='id', model=PackageInformation, redirect_url="setup:create_package_information")


# # -------------------------------------------------------------------
# #                           CouponSetting
# # -------------------------------------------------------------------


class CouponSettingCreateView(CreateView):
    template_name = "setup/coupon-setting/manage.html"
    form_class = CouponSettingManageForm

    def form_valid(self, form):
        code = form.instance.code
        field_qs = CouponSetting.objects.filter(
            code__iexact=code
        )
        result = validate_normal_form(
            field='code', field_qs=field_qs,
            form=form, request=self.request
        )
        if result == 1:
            return super().form_valid(form)
        else:
            return super().form_invalid(form)

    def get_success_url(self):
        return reverse('setup:create_coupon_setting')

    def get_context_data(self, **kwargs):
        context = super(
            CouponSettingCreateView, self
        ).get_context_data(**kwargs)
        context['page_title'] = 'Create Coupon Setting'
        context['page_short_title'] = 'Create Coupon Setting'
        context['list_objects'] = CouponSetting.objects.all().order_by('-id')
        context['list_template'] = None
        context['fields_count'] = len(
            CouponSetting._meta.get_fields()) + 1
        context['fields'] = dict([(f.name, f.verbose_name)
                                  for f in CouponSetting._meta.fields + CouponSetting._meta.many_to_many])
        context["update_url"] = "setup:update_coupon_setting"
        context["delete_url"] = "setup:delete_coupon_setting"
        context["detail_url"] = "setup:coupon_setting_detail"
        context['namespace'] = 'coupon_setting'
        context['can_add_change'] = True if self.request.user.has_perm(
            'setup.add_couponsetting') and self.request.user.has_perm('setup.change_couponsetting') else False
        context['can_view'] = self.request.user.has_perm(
            'setup.view_couponsetting')
        context['can_delete'] = self.request.user.has_perm(
            'setup.delete_couponsetting')
        return context


class CouponSettingUpdateView(UpdateView):
    template_name = "setup/coupon-setting/manage.html"
    form_class = CouponSettingManageForm

    def get_object(self):
        return get_simple_object(key="id", model=CouponSetting, self=self)

    def form_valid(self, form):
        code = form.instance.code
        self.object = self.get_object()
        if not self.object.code == code:
            field_qs = CouponSetting.objects.filter(
                code__iexact=code
            )
            result = validate_normal_form(
                field='code', field_qs=field_qs,
                form=form, request=self.request
            )
            if result == 1:
                return super().form_valid(form)
            else:
                return super().form_invalid(form)
        messages.add_message(
            self.request, messages.SUCCESS, "Coupon Setting Updated Successfully!"
        )
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('setup:create_coupon_setting')

    def get_context_data(self, **kwargs):
        context = super(
            CouponSettingUpdateView, self
        ).get_context_data(**kwargs)
        context['page_title'] = f'Update {self.get_object().code} Coupon Setting'
        context['page_short_title'] = f'Update {self.get_object().code} Coupon Setting'
        context['list_objects'] = CouponSetting.objects.all().order_by('-id')
        context['list_template'] = None
        context['fields_count'] = len(
            CouponSetting._meta.get_fields()) + 1
        context['fields'] = dict([(f.name, f.verbose_name)
                                  for f in CouponSetting._meta.fields + CouponSetting._meta.many_to_many])
        context["update_url"] = "setup:update_coupon_setting"
        context["delete_url"] = "setup:delete_coupon_setting"
        context["detail_url"] = "setup:coupon_setting_detail"
        context['namespace'] = 'coupon_setting'
        context['can_add_change'] = True if self.request.user.has_perm(
            'setup.add_couponsetting') and self.request.user.has_perm('setup.change_couponsetting') else False
        context['can_view'] = self.request.user.has_perm(
            'setup.view_couponsetting')
        context['can_delete'] = self.request.user.has_perm(
            'setup.delete_couponsetting')
        return context


class CouponSettingDetailView(DetailView):
    template_name = "snippets/detail-commonsetup/coupon-setting.html"

    def get_object(self):
        return get_simple_object(key='id', model=CouponSetting, self=self)

    def get_context_data(self, **kwargs):
        context = super(
            CouponSettingDetailView, self
        ).get_context_data(**kwargs)
        context['page_title'] = f'{self.get_object().code} - Coupon Setting Detail'
        context['page_short_title'] = f'{self.get_object().code} - Coupon Setting Detail'
        context["create_url"] = "setup:create_coupon_setting"
        context["update_url"] = "setup:update_coupon_setting"
        context["delete_url"] = "setup:delete_coupon_setting"
        context["list_url"] = "setup:create_coupon_setting"
        context['can_add_change'] = True if self.request.user.has_perm(
            'setup.add_couponsetting') and self.request.user.has_perm('setup.change_couponsetting') else False
        context['can_view'] = self.request.user.has_perm(
            'setup.view_couponsetting')
        context['can_delete'] = self.request.user.has_perm(
            'setup.delete_couponsetting')
        return context


@csrf_exempt
def delete_coupon_setting(request):
    return delete_simple_object(request=request, key='id', model=CouponSetting, redirect_url="setup:create_coupon_setting")
