"""
Django settings for cbra project.

Generated by 'django-admin startproject' using Django 1.9.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""
from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS as TCP

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import logging
import logging.handlers
from django.utils.six import moves

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
SETTINGS_DIR = os.path.dirname(__file__)
PROJECT_PATH = os.path.join(SETTINGS_DIR, os.pardir)
PROJECT_PATH = os.path.abspath(PROJECT_PATH)
TEMPLATE_PATH = os.path.join(PROJECT_PATH, 'templates')

CONFIG = moves.configparser.SafeConfigParser(allow_no_value=True)
CONFIG.read('%s\settings.cfg' % SETTINGS_DIR)


LOG_FILENAME = os.path.join(PROJECT_PATH, 'logs/cbra.log')

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': "[%(asctime)s] | %(levelname)s [%(name)s:%(lineno)s] | %(message)s",
            'datefmt': "%Y-%m-%d %H:%M:%S"
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'timedrotatingfile': {
            'level': 'DEBUG',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': LOG_FILENAME,
            'formatter': 'verbose',
            'when': 'midnight',
            'backupCount': 14
        },
    },
    'loggers': {
        'django': {
            'handlers': ['timedrotatingfile'],
            'propagate': True,
            'level': 'INFO',
        },
        'rest_framework': {
            'handlers': ['timedrotatingfile'],
            'propagate': True,
            'level': 'INFO',
        },
        'cbra': {
            'handlers': ['timedrotatingfile'],
            'level': 'INFO',
        },
        'cbraservices': {
            'handlers': ['timedrotatingfile'],
            'level': 'INFO',
        }
    }
}


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = CONFIG.get('security', 'SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = CONFIG.get('general', 'DEBUG')

ALLOWED_HOSTS = CONFIG.get('general', 'ALLOWED_HOSTS')


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'simple_history',
    'rest_framework',
    'rest_framework_extensions',
    'corsheaders',
    'cbraservices',
]

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'simple_history.middleware.HistoryRequestMiddleware',
]

ROOT_URLCONF = 'cbra.urls'

WSGI_APPLICATION = 'cbra.wsgi.application'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = 'localhost'
# EMAIL_PORT = '1025'
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'astephensonusgs@gmail.com'
EMAIL_HOST_PASSWORD = 'G30webmapseven'
DEFAULT_FROM_EMAIL = 'admin@cbra.fws.gov'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            'debug': DEBUG,
        },
    },
]


# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': CONFIG.get('databases', 'ENGINE'),
        'NAME': CONFIG.get('databases', 'NAME'),
        'USER': CONFIG.get('databases', 'USER'),
        'PASSWORD': CONFIG.get('databases', 'PASSWORD'),
        'HOST': CONFIG.get('databases', 'HOST'),
        'PORT': CONFIG.get('databases', 'PORT'),
        #'CONN_MAX_AGE': CONFIG.get('databases', 'CONN_MAX_AGE'),
        'CONN_MAX_AGE': 60,
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/New_York'

USE_I18N = False

USE_L10N = False

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

STATIC_ROOT = os.path.join(PROJECT_PATH, 'static')
STATIC_PATH = os.path.join(PROJECT_PATH, 'static/staticfiles')
STATIC_URL = '/static/'

STATICFILES_DIRS = (
    STATIC_PATH,
)

MEDIA_ROOT = os.path.join(PROJECT_PATH, 'media')
MEDIA_URL = '/media/'

CORS_ORIGIN_ALLOW_ALL = True

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        #'LOCATION': 'default-cache',
    }
}

REST_FRAMEWORK_EXTENSIONS = {
    'DEFAULT_CACHE_RESPONSE_TIMEOUT': 60 * 60,
}

# .txt - text/plain
# .pdf - application/pdf
# .doc - application/msword
# .docx - application/vnd.openxmlformats-officedocument.wordprocessingml.document
# .jpeg, .jpg - image/jpeg
# .png - image/png
# .gif - image/gif
# .tiff - image/tiff
# .bmp - image/bmp
# .zip - application/zip
# .bz - application/x-bzip
# .bz2 - application/x-bzip2
CONTENT_TYPES = ['application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
                  'application/pdf', 'text/plain', 'image/jpeg', 'image/png', 'image/gif', 'image/tiff', 'image/bmp',
                 'application/zip', 'application/x-bzip', 'application/x-bzip2']

# 2.5MB - 2621440
# 5MB - 5242880
# 10MB - 10485760
# 20MB - 20971520
# 50MB - 52428800
# 100MB 104857600
# 250MB - 262144000
# 500MB - 524288000
MAX_UPLOAD_SIZE = "2621440"
