import os
from .env import ENV_BOOL, ENV_LIST, ENV_SETTING, ABS_PATH, ENV_STR
import dj_database_url


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEBUG = ENV_BOOL('DEBUG', False)
ALLOWED_HOSTS = ENV_LIST('ALLOWED_HOSTS', ',', ['*'] if DEBUG else [])
SECRET_KEY = ENV_STR('SECRET_KEY', 'secret' if DEBUG else '')


# Application definition
INSTALLED_APPS = [
    'mail_script.apps.MailScriptConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
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

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            ABS_PATH('templates'),
        ],
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

ROOT_URLCONF = 'project.urls'
WSGI_APPLICATION = 'project.wsgi.application'
DATABASES = {'default': dj_database_url.config()}


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


# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
STATIC_URL = ENV_STR('STATIC_URL', '/static/')
STATIC_ROOT = ENV_STR('STATIC_ROOT', ABS_PATH('static'))
STATICFILES_DIRS = (
    ABS_PATH('project', 'static'),
)

MEDIA_URL = ENV_STR('MEDIA_URL', '/media/')
MEDIA_ROOT = ENV_STR('MEDIA_ROOT', ABS_PATH('', 'media'))


# Mail Script settings
GD_ROOT_DIR_ID = '1PB6dLXW_D5Z1wIFIXOKe7HaIQN2-sCub'
