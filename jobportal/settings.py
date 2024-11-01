"""
Django settings for jobportal project.

Generated by 'django-admin startproject' using Django 5.1.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

from pathlib import Path
import os
import environ

# Initialize environment variables
env = environ.Env()
environ.Env.read_env()




# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
#SECRET_KEY = os.environ.get('SECRET_KEY', '')
SECRET_KEY= 'django-insecure-q%kkrpi!o9xsz85ur!aoxth06fwye6bgjdlp40$%0hvo9rg163'


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition
#    'grappelli',
INSTALLED_APPS = [

    'django_light',
    'admin_tools_stats',  # this must be BEFORE 'admin_tools' and 'django.contrib.admin'
    'django_nvd3',
    'jazzmin',
    'cloudinary_storage',
    
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'cloudinary', #cloudinary_app
    'tailwind',
    'theme',
    'django_browser_reload',  #for automatic reloads
    'crispy_forms',
    'crispy_bootstrap4',  # Add this
    
    
    'authentication',
    'jobs',
    'notifications',
    'application_portal',
    'payment',
    
    'import_export',    #for importing and exporting data in admin
]


CLOUDINARY_STORAGE = {
    'CLOUD_NAME': 'dlwrkln6k',
    'API_KEY': '378414171715975',
    'API_SECRET': 'eQ4aV92yxESxjFr5owVUhZiN5Zg',
    
}


CRISPY_TEMPLATE_PACK = 'bootstrap4'

'''
DJANGO_ADMIN_KUBI = {
    'ADMIN_HISTORY': True,  # enables the history action panel
    'ADMIN_SEARCH': True,  # enables a full modal search
}
'''


TAILWIND_APP_NAME = 'theme'

INTERNAL_IPS = [
    "127.0.0.1",
]

NPM_BIN_PATH = "C:/Program Files/nodejs/npm.cmd"



MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    "django_browser_reload.middleware.BrowserReloadMiddleware",
    
    # append after default middlewares
    
]
#'django_auto_logout.middleware.auto_logout',    #django auto logout middleware
ROOT_URLCONF = 'jobportal.urls'

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
#'django_auto_logout.context_processors.auto_logout_client',     #django auto logout context

WSGI_APPLICATION = 'jobportal.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

"""DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}"""





#deployment database

import dj_database_url

DATABASES = {
    'default': dj_database_url.parse(env('DATABASE_URL'))
}

# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

# settings.py

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'cloudinary_storage.storage.StaticHashedCloudinaryStorage'



# Handling images
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Static files storage
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

STATICFILES_DIRS = [os.path.join(BASE_DIR, 'theme/static')]

from decouple import config

# Paystack Keys from .env file
PAYSTACK_SECRET_KEY = config('PAYSTACK_SECRET_KEY')
PAYSTACK_PUBLIC_KEY = config('PAYSTACK_PUBLIC_KEY')




# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'



#step 4
#django session timeout
"""AUTO_LOGOUT = {'IDLE_TIME': 20000, 'REDIRECT_TO_LOGIN_IMMEDIATELY': True, 
               'MESSAGE': 'The session has expired. Please login again to continue.',
               } """ # logout after 10 minutes of downtime


