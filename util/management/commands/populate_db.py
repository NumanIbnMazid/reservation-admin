from django.core.management.base import BaseCommand
from django.conf import settings
from django.contrib.sites.models import Site
from setup.models import ApplicationSetting


# $ python manage.py populate_db
class Command(BaseCommand):
    args = '<foo bar ...>'
    help = 'Seeding Initial Data'

    # Update Django Site
    def _update_default_site(self):
        application_settins_qs = ApplicationSetting.objects.all()
        if application_settins_qs.exists() and application_settins_qs.count() > 0:
            application_setting = application_settins_qs.first()
            site_qs = Site.objects.all()
            if site_qs.exists() and site_qs.count() > 0:
                site_qs.update(
                    domain=application_setting.application_domain_url, name=application_setting.application_name
                )

    # Create ApplicationSetting
    def _create_application_setting(self):
        # Default Application Settings
        if not ApplicationSetting.objects.filter(application_name__iexact='skytrip').exists():
            s_skytrip = ApplicationSetting(
                application_name='skytrip',
                application_domain_url='https://skytrip.com/',
                is_production=False,
                skytrip_address="Monihar Classic, 5th floor, 56 Shantinagar Bhashani Goli, Opposite of Naya Paltan BNP office and Near of VIP Tower, Dhaka 1217, Bangladesh",
                facebook_app_id="966529903855634",
                google_client_id="658977310896-knrl3gka66fldh83dao2rhgbblmd4un9.apps.googleusercontent.com"
            )
            s_skytrip.save()

    # destroy application settings
    def _destroy_settings(self):
        application_settins_qs = ApplicationSetting.objects.all()
        if application_settins_qs.exists() and application_settins_qs.count() > 0:
            application_settins_qs.delete()

    # Databse management handler
    def handle(self, *args, **options):
        self._create_application_setting()
        self._update_default_site()
        # destroy settings
        # self._destroy_settings()
