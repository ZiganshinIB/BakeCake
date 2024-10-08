import os
from pathlib import Path

import dj_database_url
from environs import Env

env = Env()
env.read_env()

BASE_DIR = Path(__file__).resolve().parent.parent


SECRET_KEY = env.str('DJANGO_SECRET_KEY')

DEBUG = env.bool('DJANGO_DEBUG', default=False)

ALLOWED_HOSTS = env.list('DJANGO_ALLOWED_HOSTS', default=['localhost', '127.0.0.1'])


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'cake.apps.CakeConfig',
    'rest_framework',
    'phonenumber_field',
    'djoser',

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'bakecake.urls'

if env.list("NGINX_DOMAINS", []):
    CSRF_TRUSTED_ORIGINS = env.list("NGINX_DOMAINS")
    USE_X_FORWARDED_HOST = True
    USE_X_FORWARDED_PORT = True

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'bakecake.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases
if env.str('DB_URL', ''):
    DATABASES = {
        'default': dj_database_url.config(
            default=env.str('DB_URL'),
            conn_max_age=600,
            conn_health_checks=True,
        )
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }



# Password validation

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
AUTH_USER_MODEL = 'cake.Client'

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
]

LOGIN_REDIRECT_URL = '/lk'
LOGOUT_REDIRECT_URL = '/'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.AllowAny',
    ),
    'DEFAULT_RENDER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    )

}

DJOSER = {
    'SERIALIZERS': {
        'user_create': 'cake.serializers.ClientRegistrationSerializer',
    }
}

# Internationalization

LANGUAGE_CODE = 'ru-ru'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'statics')


MEDIA_URL = 'media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

if env.str('EMAIL_HOST_USER', '') and env.str('EMAIL_HOST_PASSWORD', ''):
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST = 'smtp.gmail.com'
    EMAIL_HOST_USER = env.str('EMAIL_HOST_USER')
    EMAIL_HOST_PASSWORD = env.str('EMAIL_HOST_PASSWORD')
    EMAIL_PORT = 587
    EMAIL_USE_TLS = True
else:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Advansed settings
TLY_API_TOKEN = env.str('TLY_API_TOKEN', 'default')


