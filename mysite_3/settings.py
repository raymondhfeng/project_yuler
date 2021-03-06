"""
Django settings for mysite_3 project.

Generated by 'django-admin startproject' using Django 3.0.7.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'grm_^s^m1&m)417)6t2@5onj)su-xu3&w=u6azf+e#eb5up#u8'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['django-project-yuler.eba-pcnmv7m3.us-west-2.elasticbeanstalk.com','e3726eaab85e.ngrok.io','71747286822b.ngrok.io','92bc709bb4bf.ngrok.io','8afdce4bb3a3.ngrok.io','058a7295c294.ngrok.io','54ab765a3bf6.ngrok.io','23cdf674e978.ngrok.io','45471f846089.ngrok.io','eab44cb79223.ngrok.io','d2ac2bf534a4.ngrok.io', '60e8fb50f3d2.ngrok.io' ,'0c36d91605b6.ngrok.io','dbc0fc93ea18.ngrok.io', '127.0.0.1']

INTERNAL_IPS = ['71.202.181.19','127.0.0.1']

# Application definition

INSTALLED_APPS = [
    'ignition.apps.IgnitionConfig',
    'chartjs',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'debug_toolbar'
    ]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    ]

ROOT_URLCONF = 'mysite_3.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'mysite_3.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'test',
        'USER': 'pi',
        'PASSWORD': 'raspberry',
        'HOST': 'localhost',
        'PORT': '',
    }
    # 'default': {
    #    'ENGINE': 'django.db.backends.sqlite3', # TODO: Eventually change this to postgres 
    #    'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    # }
}


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'US/Pacific'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'


# Celery application definition
# http://docs.celeryproject.org/en/v4.0.2/userguide/configuration.html
CELERY_BROKER_URL = 'redis://localhost:6379'
CELERY_RESULT_BACKEND = 'redis://localhost:6379'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TASK_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Asia/Makassar'

from celery.schedules import crontab

CELERY_BEAT_SCHEDULE = {
    'task-number-one': {
        'task': 'ignition.tasks.task_number_one',
        'schedule': crontab(minute="*/1"),
    }, 
    'task-number-two': {
        'task': 'ignition.tasks.task_number_two',
        'schedule': crontab(minute="*/1")
    },
    'clean_screenshots': {
        'task': 'ignition.tasks.clean_screenshots',
        'schedule': crontab(hour=0)
    },
    'stitch_photos': {
        'task': 'ignition.tasks.stitch_photos',
        'schedule': crontab(minute="*/1")
    },
    'check_ignition_timeout': {
        'task': 'ignition.tasks.check_ignition_timeout',
        'schedule': crontab(minute="*/1")
    }
}
