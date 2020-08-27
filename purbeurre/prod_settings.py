import os

from .settings import *
# Sentry
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

sentry_sdk.init(
    dsn="https://da7ff0a617ee4327afaf9b54fdac9971@o435771.ingest.sentry.io/5395667",
    integrations=[DjangoIntegration()],

    # If you wish to associate users to errors (assuming you are using
    # django.contrib.auth) you may enable sending PII data.
    send_default_pii=True
)

# debug
DEBUG = False
TEMPLATE_DEBUG = False

# disable django debug toolbar
INTERNAL_IPS = []

# security
ALLOWED_HOSTS = ['*', ]
SECRET_KEY = get_env_variable('SECRET_KEY', '')

# postgres database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'purbeurre',
        'USER': 'jmlm',
        'PASSWORD': 'jmlmpw',
        'HOST': 'db',
        'PORT': '5432',
    }
}
WSGI_APPLICATION = 'purbeurre.wsgi.application'

# static files
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
# white noise for static files
MIDDLEWARE += ['whitenoise.middleware.WhiteNoiseMiddleware']
STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'
