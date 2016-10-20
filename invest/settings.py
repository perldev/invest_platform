"""
Django settings for banksite project.

Generated by 'django-admin startproject' using Django 1.9.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '$v7-la=pobfja&9g&^i)e=o07-4oo5x7e!3w2c1-qci32bage2'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
DEFAULT_CURRENCY=1
BANK_ACCOUNT = 1
INVESTMENT_ACCOUNT = 2
PERCENT_ACCOUNT = 3
ACCOUNT_ACTIVATION_DAYS = 7

COMPANY_NAME = "MicroCredit Georgia Mame"
COMPANY_TAXID = "123143120"
COMPANY_REGID = "9834123"
COMPANY_BANK = "TBC"
COMPANY_ACC = "GL121239011231"
COMPANY_COUNTRY = "Georgia"
COMPANY_CITY = "Tbilisi"
COMPANY_ADDR = "Write here something where are you"

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    # ... include the providers you want to enable:
#    'allauth.socialaccount.providers.amazon',
#    'allauth.socialaccount.providers.angellist',
#    'allauth.socialaccount.providers.asana',
#    'allauth.socialaccount.providers.baidu',
#    'allauth.socialaccount.providers.basecamp',
#    'allauth.socialaccount.providers.bitbucket',
#    'allauth.socialaccount.providers.bitbucket_oauth2',
 #   'allauth.socialaccount.providers.bitly',
  #  'allauth.socialaccount.providers.coinbase',
   # 'allauth.socialaccount.providers.digitalocean',
   # 'allauth.socialaccount.providers.douban',
   # 'allauth.socialaccount.providers.draugiem',
  #  'allauth.socialaccount.providers.dropbox',
  #  'allauth.socialaccount.providers.dropbox_oauth2',
  #  'allauth.socialaccount.providers.edmodo',
  #  'allauth.socialaccount.providers.eveonline',
  #  'allauth.socialaccount.providers.evernote',
    'allauth.socialaccount.providers.facebook',
  #  'allauth.socialaccount.providers.feedly',
    'allauth.socialaccount.providers.flickr',
   # 'allauth.socialaccount.providers.foursquare',
   # 'allauth.socialaccount.providers.fxa',
    'allauth.socialaccount.providers.github',
   # 'allauth.socialaccount.providers.gitlab',
    'allauth.socialaccount.providers.google',
   # 'allauth.socialaccount.providers.hubic',
  #  'allauth.socialaccount.providers.instagram',
    'allauth.socialaccount.providers.linkedin',
    'allauth.socialaccount.providers.linkedin_oauth2',
    'allauth.socialaccount.providers.mailru',
    'allauth.socialaccount.providers.odnoklassniki',
    'allauth.socialaccount.providers.openid',
   # 'allauth.socialaccount.providers.orcid',
   # 'allauth.socialaccount.providers.paypal',
   # 'allauth.socialaccount.providers.persona',
   # 'allauth.socialaccount.providers.pinterest',
   # 'allauth.socialaccount.providers.reddit',
   # 'allauth.socialaccount.providers.robinhood',
   # 'allauth.socialaccount.providers.shopify',
   # 'allauth.socialaccount.providers.slack',
   # 'allauth.socialaccount.providers.soundcloud',
   # 'allauth.socialaccount.providers.spotify',
   # 'allauth.socialaccount.providers.stackexchange',
   # 'allauth.socialaccount.providers.stripe',
   # 'allauth.socialaccount.providers.tumblr',
   # 'allauth.socialaccount.providers.twentythreeandme',
   # 'allauth.socialaccount.providers.twitch',
    'allauth.socialaccount.providers.twitter',
   # 'allauth.socialaccount.providers.untappd',
   # 'allauth.socialaccount.providers.vimeo',
    'allauth.socialaccount.providers.vk',
  #  'allauth.socialaccount.providers.weibo',
  #  'allauth.socialaccount.providers.weixin',
  #  'allauth.socialaccount.providers.windowslive',
  #  'allauth.socialaccount.providers.xing',


    'flat',
    'rest_framework',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',

    # 'django.contrib.staticfiles',
    'startpage'
]

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': ('rest_framework.permissions.IsAdminUser',),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 10
}

STATIC_URL = "/static/"

if not DEBUG:
    INSTALLED_APPS += 'django.contrib.staticfiles'
    STATIC_URL = "/static/"


MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

AUTHENTICATION_BACKENDS = (
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',

    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
)

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': ('rest_framework.permissions.AllowAny',),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 10
}


ROOT_URLCONF = 'invest.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR + "/tmpl"],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'startpage.views.context_processor',
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'invest.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

MEDIA_ROOT = BASE_DIR + "media"

MEDIA_URL = "/media/"
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, "static")

MEDIA_ROOT = os.path.join(BASE_DIR, "media")

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'filters': {
       'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'propagate': True,
        },
        'django.db.backends': {
            'level': 'DEBUG',
            'handlers': ['console'],
        },

    }
}

SITE_ID = 1