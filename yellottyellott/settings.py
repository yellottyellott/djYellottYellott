from os.path import dirname, join
from django.conf.global_settings import *   # NOQA


DEBUG = TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_TZ = True
USE_I18N = True
USE_L10N = True

SECRET_KEY = 'scm29^_i#%mgq_z0dwwfal#6pr*(l9pd$!sn7lels+g=rm9939'


WSGI_APPLICATION = 'yellottyellott.wsgi.application'

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE_CLASSES = list(MIDDLEWARE_CLASSES) + [
]

ROOT_URLCONF = 'yellottyellott.urls'


BASE_DIR = dirname(dirname(__file__))

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    join(BASE_DIR, 'yellottyellott', 'static'),
]

TEMPLATE_DIRS = [
    join(BASE_DIR, 'yellottyellott', 'templates'),
]
