"""
Django settings for AdminDashboardService project.

Generated by 'django-admin startproject' using Django 4.2.10.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path
import os
import dj_database_url

# settings.py
# Q_CLUSTER = {
#     'name': 'DjangoQCluster',
#     'workers': 4,
#     'recycle': 500,
#     'timeout': 60,
#     'django_redis': 'default',  # Optional if using Redis
# }

# Build paths inside the project like this: BASE_DIR / 'subdir'.
# BASE_DIR = Path(__file__).resolve().parent.parent
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY="django-insecure-p07mtuuqn&30g@)e6*r&fpkdl_i5^y4*=3#d57ka66b$6jx==e"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = "true"#os.environ.get('DEBUG', "False").lower() == "true"


#ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS").split(" ")
# ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", "localhost").split(" ")

ALLOWED_HOSTS=['localhost','127.0.0.1','159.89.164.235','dashboard.cabriot.com']


# Application definition

INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'AdminDashboard',
    'MentorDashboard',
    'account',
    'rest_framework',
    'rest_framework_simplejwt',
   'django_rest_passwordreset',
    'corsheaders',
    'import_export',
    "django_browser_reload",

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # "django_browser_reload.middleware.BrowserReloadMiddleware",
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'MentorDashboard.middleware.BranchCompanyMiddleware',
    'MentorDashboard.middleware.RestrictAdminMiddleware',

]

ROOT_URLCONF = 'AdminDashboardService.urls'
LOGIN_URL = 'mentor_login' 

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

WSGI_APPLICATION = 'AdminDashboardService.wsgi.application'
AUTH_USER_MODEL = 'account.CustomUser'

import os

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': os.environ.get('DB_NAME', 'cb'),
#         'USER': os.environ.get('DB_USER', 'postgres'),
#         'PASSWORD': os.environ.get('DB_PASSWORD', 'root'),
#         'HOST': os.environ.get('DB_HOST', 'localhost'),
#         'PORT': os.environ.get('DB_PORT', '5432'),
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'cabriot',
        'USER': 'etech',
        'PASSWORD': 'nandi1234$',
        'HOST': 'localhost',
        'PORT': '',
    }
}

# DB_NAME=cabriot
# DB_USER=etech
# DB_PASSWORD=nandi1234$
# DB_HOST=localhost
# DB_PORT=5432
# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.postgresql",
#         "NAME": os.environ.get('DB_NAME'),
#         "USER": os.environ.get('DB_USER'),
#         "PASSWORD": os.environ.get('DB_USER_PASSWORD'),
#         "HOST": os.environ.get('DB_HOST'),
#         "PORT": os.environ.get('DB_PORT'),
#     }
# }


#link with render database
# DATABASES = {'default': dj_database_url.config(default=os.environ.get('DATABASE_URL'))}



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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kolkata'  # Indian Standard Time (IST)
USE_TZ = True  # Enable timezone-aware datetime


USE_I18N = True




# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
STATIC_ROOT=os.path.join(BASE_DIR,'staticfiles')

# CORS_ALLOWED_ORIGINS = [
#      'https://cabriot-dashboard-staging.vercel.app/',
#        "35.160.120.126",
#        'http://localhost:5173',
#        "44.233.151.27",
#        "34.211.200.85"
# ]

CORS_ALLOWED_ORIGINS = [
    'https://cabriot-admin-frontend.vercel.app',  # Remove the trailing slash
    'http://35.160.120.126',  # Add 'http://' or 'https://'
    'http://44.233.151.27',  # Add 'http://' or 'https://'
    'http://34.211.200.85',  # Add 'http://' or 'https://'
    'http://localhost:5173',
    'http://localhost:8000',
    'http://localhost:8001',
    'http://159.89.164.235:8000',
    'http://159.89.164.235:8001',
    'http://localhost:8001',
    'http://127.0.0.1:8001',
    'http://dashboard.cabriot.com',
]

# Optional: Allow all methods and headers
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True
CSRF_COOKIE_HTTPONLY = False  # Allow JavaScript to access the CSRF cookie

CSRF_TRUSTED_ORIGINS = [
    'http://localhost:8001',
    'http://127.0.0.1:8001',
    'http://159.89.164.235:8000'
    'http://159.89.164.235:8001',  # Add other domains you need
    'https://dashboard.cabriot.com'
]

# CSRF_TRUSTED_ORIGINS=True
# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
# settings.py
import os

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),  # Add MentorDashboard templates
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



JAZZMIN_SETTINGS = {
    "site_title": "Cabriot Dashboard",
    "site_header": "Cabriot Dashboard",
    "site_brand": "Cabriot",
    "site_icon": "fas fa-globe",
    "welcome_sign": "Welcome to Cabriot Dashboard",
    "copyright": "Cabriot",
}