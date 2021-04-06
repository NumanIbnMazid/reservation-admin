from django.urls import path, include
from .views import (
    VisaInformationCreateView, VisaInformationUpdateView, VisaInformationDetailView, delete_visa_information,
    SSLcommerzConfCreateView, SSLcommerzConfUpdateView, SSLcommerzConfDetailView, delete_ssl_commerz_conf,
    ApplicationSettingUpdateView, ApplicationSettingDetailView,
    PackageInformationCreateView, PackageInformationUpdateView, PackageInformationDetailView, delete_package_information, 
    CouponSettingCreateView, CouponSettingUpdateView, CouponSettingDetailView, delete_coupon_setting
)

urlpatterns = [
    # # -------------------------------------------------------------------
    # #                           VisaInformation
    # # -------------------------------------------------------------------
    path("create-visa-information/", VisaInformationCreateView.as_view(), name="create_visa_information"),
    path("update-visa-information/<id>/", VisaInformationUpdateView.as_view(), name="update_visa_information"),
    path("visa-information/<id>/detail/", VisaInformationDetailView.as_view(), name="visa_information_detail"),
    path("delete-visa-information/", delete_visa_information, name="delete_visa_information"),
    # # -------------------------------------------------------------------
    # #                           SSLcommerzConf
    # # -------------------------------------------------------------------
    path("create-ssl-commerz-conf/", SSLcommerzConfCreateView.as_view(), name="create_ssl_commerz_conf"),
    path("update-ssl-commerz-conf/<id>/", SSLcommerzConfUpdateView.as_view(), name="update_ssl_commerz_conf"),
    path("ssl-commerz-conf/<id>/detail/", SSLcommerzConfDetailView.as_view(), name="ssl_commerz_conf_detail"),
    path("delete-ssl-commerz-conf/", delete_ssl_commerz_conf, name="delete_ssl_commerz_conf"),
    # # -------------------------------------------------------------------
    # #                           ApplicationSetting
    # # -------------------------------------------------------------------
    path("update-application-setting/<id>/", ApplicationSettingUpdateView.as_view(), name="update_application_setting"),
    path("application-setting-detail/<id>/", ApplicationSettingDetailView.as_view(), name="application_setting_detail"),
    # # -------------------------------------------------------------------
    # #                           PackageInformation
    # # -------------------------------------------------------------------
    path("create-package-information/", PackageInformationCreateView.as_view(), name="create_package_information"),
    path("update-package-information/<id>/", PackageInformationUpdateView.as_view(), name="update_package_information"),
    path("package-information/<id>/detail/", PackageInformationDetailView.as_view(), name="package_information_detail"),
    path("delete-package-information/", delete_package_information, name="delete_package_information"),
    # # -------------------------------------------------------------------
    # #                           CouponSetting
    # # -------------------------------------------------------------------
    path("create-coupon/", CouponSettingCreateView.as_view(), name="create_coupon_setting"),
    path("update-coupon/<id>/", CouponSettingUpdateView.as_view(), name="update_coupon_setting"),
    path("coupon/<id>/detail/", CouponSettingDetailView.as_view(), name="coupon_setting_detail"),
    path("delete-coupon/", delete_coupon_setting, name="delete_coupon_setting"),
]
