import os
from pathlib import Path
from django.conf import settings
from django.contrib import staticfiles
from trustly.services.elastic_manager.elastic_controller import elastic_controller
from trustly.services.state_manager.states import APP_STATUS
import mimetypes

mimetypes.add_type("image/svg+xml", ".svg", True)
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-ir+r3)d@v53u&qw-gfo&)&z%vda+scaq+0gw)9@u%zpjadip!3'

DEBUG = APP_STATUS.S_DEVELOPER

ALLOWED_HOSTS = ['*']
CSRF_TRUSTED_ORIGINS = [
  'http://localhost',
  'http://127.0.0.1',
  'http://localhost:3000',
  'http://localhost:8080',
  'http://localhost:8080',
  'http://127.0.0.1:8080',
  'http://0.0.0.0:8070',
]

INSTALLED_APPS = [
  'django.contrib.admin',
  'django.contrib.auth',
  'django.contrib.contenttypes',
  'django.contrib.sessions',
  'django.contrib.messages',
  'django.contrib.staticfiles',
  'trustly'
]

MIDDLEWARE = [
  'django.middleware.security.SecurityMiddleware',
  'django.contrib.sessions.middleware.SessionMiddleware',
  'django.middleware.common.CommonMiddleware',
  'django.middleware.csrf.CsrfViewMiddleware',
  'django.contrib.auth.middleware.AuthenticationMiddleware',
  'django.contrib.messages.middleware.MessageMiddleware',
  'trustly.middleware.maintenance_mode_middleware.maintenance_mode_middleware',
  'trustly.middleware.notification_routes_direct_access.notification_routes_direct_access',
  'trustly.middleware.cms_session_security.cms_session_security',
  'trustly.middleware.encrypted_access_filter.EncryptedAccessFilter',
  'trustly.middleware.service_ready_middleware.service_ready_middleware',
]
ROOT_URLCONF = 'trustly.urls'

SESSION_COOKIE_AGE = 600
SESSION_SAVE_EVERY_REQUEST = True
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'None'
SESSION_COOKIE_SECURE = True


TEMPLATES = [
  {
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'DIRS': [os.path.join(BASE_DIR, 'trustly/templates')]
    ,
    'APP_DIRS': True,
    'OPTIONS': {
      'context_processors': [
        'django.template.context_processors.debug',
        'django.template.context_processors.request',
        'django.template.context_processors.csrf',
        'django.template.context_processors.static',
        'django.contrib.auth.context_processors.auth',
        'django.contrib.messages.context_processors.messages'
      ],
    },
  },
]

WSGI_APPLICATION = 'trustly.wsgi.application'

DATABASES = {
  'default': {
    'ENGINE': 'django.db.backends.sqlite3',
    'NAME': BASE_DIR / 'db.sqlite3',
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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]