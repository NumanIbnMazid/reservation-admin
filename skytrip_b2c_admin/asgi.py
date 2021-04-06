"""
ASGI config for skytrip_b2c_admin project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/asgi/
"""

import os
from decouple import config, Csv

from django.core.asgi import get_asgi_application

if config('IS_PRODUCTION', default=False, cast=bool) == True:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'skytrip_b2c_admin.settings.production')
else:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'skytrip_b2c_admin.settings.development')

application = get_asgi_application()
