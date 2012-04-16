# -*- coding: utf-8 -*-
import os, sys

MY_DJANGO_ROOT = os.sep.join(os.path.dirname(os.path.realpath(__file__)).split(os.sep)[:-2])
PROJECT_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.append(MY_DJANGO_ROOT)
sys.path.append(MY_DJANGO_ROOT+'/apps')
sys.path.append(PROJECT_DIR)

from common.settings import *

ADMINS = (
    ('Alexey', 'chukreev.alexey@gmail.com'),
)

DEBUG = False
TEMPLATE_DEBUG = DEBUG

PROJECT_NAME = 'sails'
PROJECT_TITLE = u'Учетная программа "Натали Турс"'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'sails',
        'USER': 'sails',
        'PASSWORD': 'F6Hked7hgkl',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

SITE_ID=1

MEDIA_URL = '/media/'
MEDIA_ROOT = PROJECT_DIR + '/media/'

STATIC_URL = MEDIA_URL
STATIC_ROOT = MEDIA_ROOT

ADMIN_MEDIA_PREFIX = '/admin_media/'
ADMIN_MEDIA_ROOT = MY_DJANGO_ROOT + '/admin_media/'

AUTOCOMPLETE_MEDIA_PREFIX = MEDIA_URL + 'jquery/'

SECRET_KEY = 'k0!2x-1^zh^+8b(a6*!%o@d#_xe3k=aj1(5q3x9oit-)3)l%z8'

ROOT_URLCONF = '%s.urls' % PROJECT_NAME

TEMPLATE_DIRS = (
    #MY_DJANGO_ROOT + "/apps/common/templates",
    PROJECT_DIR + "/website/templates",
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'website.middleware.BeforeViewMiddleware',
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.admin',
    'django.contrib.sites',
    'common',
    'south',
    'website',
)

#AUTH
AUTH_PROFILE_MODULE = 'website.Staff'
LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/'

# MESSAGES
MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'

# CAPTCHA SETTINGS
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': '%s/cache' % PROJECT_DIR,
        'TIMEOUT': 60,
        'OPTIONS': {
            'MAX_ENTRIES': 1000
        }
    }
    #'default': {
    #    'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
    #    'KEY_PREFIX': PROJECT_NAME,
    #    'LOCATION': '127.0.0.1:11211',
    #},
    #'default': {
    #    'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    #}
}

CAPTCHA_CACHE_PREFIX = PROJECT_NAME+"_captcha_"
