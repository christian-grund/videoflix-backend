"""
Django settings for videoflix project.

Generated by 'django-admin startproject' using Django 5.1.1.
"""

import os
from pathlib import Path
from decouple import config
import ssl
import certifi

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-^b-ugi2=(7k2x2g9oiw2m9*#*vlv%uobcpu@o9$))m8ma@4k03'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = [  
    'http://localhost:4200/',
    'localhost',
    '127.0.0.1',
    '34.159.98.222',
    'videoflix-backend.christian-grund.dev'
    ]


# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework.authtoken', 
    'corsheaders',
    'content.apps.ContentConfig',
    'debug_toolbar',
    'django_rq',
    'import_export',
    'user',
]

MIDDLEWARE = [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'videoflix.middlewares.AddAcceptRangesHeaderMiddleware',
]

# CORS_ALLOW_ALL_ORIGINS = True

CORS_ALLOWED_ORIGINS = [
    "https://videoflix.christian-grund.dev",
    "http://localhost:4200",  # Lokale Entwicklung
]

CORS_ALLOW_CREDENTIALS = True

CACHE_TTL = 60 * 15 

CACHES = {    
    "default": {        
        "BACKEND": "django_redis.cache.RedisCache",        
        "LOCATION": "redis://127.0.0.1:6379/1",        
        "OPTIONS": {  
            "PASSWORD":'foobared',          
            "CLIENT_CLASS": "django_redis.client.DefaultClient"        
            },        
        "KEY_PREFIX": "videoflix"    
    }
}

INTERNAL_IPS = [
    "127.0.0.1",
]

# default: standardmäßige Aufgaben
# with-sentinel: Teil von Redis, womit Sachen besser laufen
RQ_QUEUES = {
    'default': {
        'HOST': 'localhost',
        'PORT': 6379,
        'DB': 0,
        # 'USERNAME': 'some-user',
        # 'PASSWORD': 'foobared',
        'DEFAULT_TIMEOUT': 360,
        # 'REDIS_CLIENT_KWARGS': {    # Eventual additional Redis connection arguments
        #     'ssl_cert_reqs': None,
        # },
    },
}

# RQ_EXCEPTION_HANDLERS = ['path.to.my.handler'] # If you need custom exception handlers

ROOT_URLCONF = 'videoflix.urls'

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

# MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'
MEDIA_ROOT = '/var/www/videoflix-backend/media'

WSGI_APPLICATION = 'videoflix.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'videoflix_database',
        'USER': 'chris',
        'PASSWORD': '1234', 
        'HOST': 'localhost', 
        # 'PORT': '',  
        'PORT': '5432',  # Der Standard-Port für PostgreSQL
    },
    'test': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'test_videoflix',
        'USER': 'dein_benutzername',
        'PASSWORD': 'dein_passwort',
        'HOST': 'localhost',
        'PORT': '5432',
    },
}


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    # {
    #     'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    # },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    # },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    # },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    # },
]


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = '/static/'

# STATIC_ROOT = BASE_DIR / 'static/staticfiles'
STATIC_ROOT = os.path.join(BASE_DIR, "static/staticfiles")

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'), 
]


# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',  # Ensure JSON responses
    ),
}

IMPORT_EXPORT_USE_TRANSACTIONS = True

AUTH_USER_MODEL = 'user.CustomUser'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 465  
EMAIL_USE_TLS = False  
EMAIL_USE_SSL = True  
# EMAIL_HOST_USER = config('EMAIL_HOST_USER')
# EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
EMAIL_HOST_USER = 'grund7@gmail.com'
EMAIL_HOST_PASSWORD = 'xhlq qrxb aymi pimv'


ssl_context = ssl.create_default_context(cafile=certifi.where())


