"""
Django settings for shrubbery project.

Generated by 'django-admin startproject' using Django 4.2.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""
import os

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
if os.environ.get('SHRUBBERY_ENV') == 'prd':
    SECRET_KEY = os.environ['DJANGO_SECRET_KEY']
    ADMIN_ENABLED = False
else:
    SECRET_KEY = "development-dummy-secret-key"
    ADMIN_ENABLED = True

# SECURITY WARNING: don't run with debug turned on in production!
if os.environ.get('SHRUBBERY_ENV') == 'prd':
    ALLOWED_HOSTS = ['shrubbery.onrender.com', 'localhost']
    CSRF_TRUSTED_ORIGINS = ['https://shrubbery.onrender.com']
else:
    ALLOWED_HOSTS = ['*']

if os.environ.get('SHRUBBERY_ENV') == 'prd':
    DEBUG = False
else:
    DEBUG = True


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_bootstrap5',
    'django_seed',
    'sass_processor',
    'comments',
    'resources',
    'homeworks',
    'homeworksolutions',
    'challenges',
    'challengesolutions',
    'exams',
    'vouchers',
    'points',
    'users',
    'news',
    'materials',
    'forum',
    'activity',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'shrubbery.middlewares.TimezoneMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware'
]

ROOT_URLCONF = 'shrubbery.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'shrubbery/templates', 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            'libraries': {
                'extras': 'shrubbery.templatetags.extras',
            },
        },
    },
]

WSGI_APPLICATION = 'shrubbery.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

if os.environ.get('SHRUBBERY_ENV') == 'prd':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.environ['POSTGRES_DB_NAME'],
            'USER': os.environ['POSTGRES_USER'],
            'PASSWORD': os.environ['POSTGRES_PASSWORD'],
            'HOST': os.environ['POSTGRES_HOSTNAME'],
            'PORT': '5432',
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'bg'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

INTERFACE_TZ = 'Europe/Sofia'


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'sass_processor.finders.CssFinder',
]


STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'static'

STATICFILES_DIRS = [
    BASE_DIR / "shrubbery/static",
    BASE_DIR / "shrubbery/static/scss",
    BASE_DIR / "media",
]

if os.environ.get('SHRUBBERY_ENV') == 'prd':
    SASS_PROCESSOR_ROOT = BASE_DIR / 'static'
else:
    SASS_PROCESSOR_ROOT = BASE_DIR / 'shrubbery/static/scss'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Overwrite default user model

AUTH_USER_MODEL = 'users.User'


# Media files for uploading resources

MEDIA_URL = '/media/' 
MEDIA_ROOT = BASE_DIR / 'media'

# Default endpoints
LOGIN_URL = '/login'

# Celery and Redis setup
CELERY_BROKER_URL = 'redis://localhost:6379'
CELERY_RESULT_BACKEND = 'redis://localhost:6379'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = TIME_ZONE
