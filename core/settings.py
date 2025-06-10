from pathlib import Path
import datetime
import os

import cloudinary
import cloudinary.uploader
import cloudinary.api

from decouple import config


BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = config('API_SECRET_KEY')
DEBUG = True
ALLOWED_HOSTS = ["*"]


SHARED_APPS = (
    'django_tenants',
    'tenants',
    # "admin_interface",
    'django.contrib.contenttypes',
   
    
)

TENANT_APPS = (
    'django.contrib.contenttypes',
    'django.contrib.auth',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.admin',
    'django.contrib.staticfiles',
    'rest_framework_simplejwt',
    'rest_framework',
    'simple_history',
    'cloudinary',
    'drf_yasg',
    'corsheaders',
    'colorfield',
    'django_filters',    
    'accounts',
    'appAdmin'
)

INSTALLED_APPS = list(SHARED_APPS) + \
    [app for app in TENANT_APPS if app not in SHARED_APPS]


MIDDLEWARE = [
    'django_tenants.middleware.main.TenantMainMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'simple_history.middleware.HistoryRequestMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
]


SESSION_EXPIRE_SECONDS = 1800  # 1/2 hour
SESSION_EXPIRE_AFTER_LAST_ACTIVITY = True
SESSION_TIMEOUT_REDIRECT = 'accounts/login'

ROOT_URLCONF = 'core.urls'

X_FRAME_OPTIONS = "SAMEORIGIN"


TENANT_MODEL = "tenants.Client"
TENANT_DOMAIN_MODEL = "tenants.Domain"

DATABASE_ROUTERS = (
    'django_tenants.routers.TenantSyncRouter',
)


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates'),],
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

WSGI_APPLICATION = 'core.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': config('ENGINE_DB'),
        'NAME': config('NAME_DB'),
        'USER': config('USER_DB'),
        'PASSWORD': config('PASSWORD_DB'),
        'HOST': config('HOST_DB'),
        'PORT': config('PORT_DB'),
    }
}

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
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'es-ES'
TIME_ZONE = 'America/Bogota'
USE_I18N = True
USE_L10N = True
USE_TZ = True


cloudinary.config(
    cloud_name = config('NAME_CD'),
    api_key = config('APY_KEY_CD'),
    api_secret = config('APY_SECRET_CD'),
    #   secure = true
)


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
AUTH_USER_MODEL = 'accounts.Account'

CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_ALL_ORIGINS = True
CARS_ALLOW_CREDENCIALS = True


SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': datetime.timedelta(days=100)
}

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    )
}

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_TMP = os.path.join(BASE_DIR, 'static')
STATIC_URL = '/static/'

os.makedirs(STATIC_TMP, exist_ok=True)
os.makedirs(STATIC_ROOT, exist_ok=True)

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)


CELERY_TASK_ROUTES = {
    'core.tasks.process_incoming_message': {'queue': 'default'},
    'core.tasks.send_whatsapp_message': {'queue': 'default'},
}

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            'hosts': [('localhost', 6379)],
        },
    },
}