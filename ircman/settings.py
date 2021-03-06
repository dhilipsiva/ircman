"""
Django settings for ircman project.

Generated by 'django-admin startproject' using Django 1.8.1.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

try:
    from local_settings import BASE_DIR
except ImportError:
    BASE_DIR = os.path.dirname(os.path.abspath(os.path.abspath(__file__)))

INDEX_HTML = os.path.join(BASE_DIR, 'generated/index.html')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!

try:
    from local_settings import SECRET_KEY
except ImportError:
    SECRET_KEY = 'd#o&k1n_58i0qn_)+vg#j5!e=b%lq*p2^qc5fmut_lfo9dun5_'


# SECURITY WARNING: don't run with debug turned on in production!
try:
    from local_settings import DEBUG
except ImportError:
    DEBUG = False

ALLOWED_HOSTS = [
    'localhost:8100',
    '127.0.0.1:8100',
    '127.0.0.1',
    'localhost',
    '0.0.0.0',
    'ircman.co',
]

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'tokenapi',
    'corsheaders',

    # Custom apps
    'core',
)

if DEBUG:
    INSTALLED_APPS += (
        'django_extensions',
    )

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

ROOT_URLCONF = 'ircman.urls'

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
        },
    },
]

WSGI_APPLICATION = 'ircman.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases
try:
    from local_settings import DATABASES
except ImportError:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }

# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/static/'

AUTH_USER_MODEL = 'core.User'

try:
    from local_settings import BROKER_URL
except ImportError:
    BROKER_URL = 'amqp://guest:guest@localhost:5672//'


try:
    from local_settings import REDIS_HOST, REDIS_PORT
except ImportError:
    # This should also be changed in sockets/index.js
    REDIS_HOST = "0.0.0.0"
    REDIS_PORT = 6379

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'tokenapi.backends.TokenBackend'
)

CORS_ORIGIN_WHITELIST = (
    '0.0.0.0:4200',
)


STATIC_ROOT = os.path.join(BASE_DIR, 'static')
