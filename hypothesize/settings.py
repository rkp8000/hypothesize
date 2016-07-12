"""
Django settings for hypothesize project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)

import os

import my_settings

BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!

# SECURITY WARNING: don't run with debug turned on in production!

DEBUG = True

ALLOWED_HOSTS = ['*']

# set default settings or override with user-defined settings in my_settings.py

if my_settings.USERNAME:

    BASICAUTH_USERNAME = my_settings.USERNAME

else:

    BASICAUTH_USERNAME = 'user'

if my_settings.PASSWORD:

    BASICAUTH_PASSWORD = my_settings.PASSWORD

else:

    BASICAUTH_PASSWORD = 'pass'

if my_settings.TOPIC_DIRECTORY:

    TOPIC_SAVE_DIRECTORY = my_settings.TOPIC_DIRECTORY

else:

    TOPIC_SAVE_DIRECTORY = os.path.join(BASE_DIR, 'topics')

if my_settings.DATABASE_BACKUP_DIRECTORY:

    DATABASE_BACKUP_DIRECTORY = my_settings.DATABASE_BACKUP_DIRECTORY

else:

    DATABASE_BACKUP_DIRECTORY = os.path.join(BASE_DIR, 'db_backups')

DATABASE_BACKUP_INTERVAL_SECONDS = 24 * 60 * 60

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'hypothesize_app'
)

MIDDLEWARE_CLASSES = (
    'hypothesize_app.auth.BasicAuthMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'hypothesize.urls'

WSGI_APPLICATION = 'hypothesize.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

MEDIA_URL = '/media/'
STATIC_URL = '/static/'

# Typically these end up symlinks on prod boxes

STATIC_ROOT = os.path.join(BASE_DIR, 'static')
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Try to import local settings

try:
    from local_settings import *
except ImportError:
    pass

# Finally, if there is no secret key defined, create one now.

try:

    SECRET_KEY

except NameError:

    SECRET_FILE = os.path.join(BASE_DIR, '../../secret.txt')

    try:

        SECRET_KEY = open(SECRET_FILE).read().strip()

    except IOError:

        try:

            import random

            SECRET_KEY = ''.join([random.SystemRandom().choice('abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)') for i in range(50)])
            secret = file(SECRET_FILE, 'w')
            secret.write(SECRET_KEY)
            secret.close()

        except IOError:

            Exception('Please create a %s file with random characters \
            to generate your secret key!' % SECRET_FILE)

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                # Insert your TEMPLATE_CONTEXT_PROCESSORS here or use this
                # list if you haven't customized them:
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]