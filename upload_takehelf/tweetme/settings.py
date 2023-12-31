


from lib2to3.pytree import Base
from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# print(BASE_DIR,".................")
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-0leuv-+3_$=)$8mm9boqrk1#yh+e89s*#-179-(d)z+_zpe*jq'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# ALLOWED_HOSTS = ['127.0.0.1', '.mydomain.com','localhost']
LOGIN_URL="/login"
MAX_TWEET_LENGTH= 240 
TWEET_ACTION_OPTIONS =["like", "unlike", "retweet"]






INSTALLED_APPS = [
    # 'daphne',
    # 'channels',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'twapp',
    'rest_framework',
    'corsheaders',
    'rest_framework.authtoken',
    
]




MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    # 'twapp.middleware.SpaCyMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    
    
    
]

CSRF_COOKIE_SECURE = False

# Set 'CSRF_COOKIE_HTTPONLY' to True for extra security
CSRF_COOKIE_HTTPONLY = False

# Set 'CSRF_COOKIE_SAMESITE' to 'Lax' or 'Strict' for proper CSRF protection
CSRF_COOKIE_SAMESITE = 'Lax'  # 'Lax' allows cross-origin requests from GET methods

# Allow AJAX requests from the frontend to access the CSRF cookie
# CSRF_TRUSTED_ORIGINS = ["http://localhost:3000","http://127.0.0.1:3000"]
# CORS_ORIGIN_WHITELIST=[
#     "http://localhost:3000",
#     "http://127.0.0.1:3000",
   
# ]
# CORS_ALLOW_ORIGINS=[
#     'http://localhost:3000',
#     "http://127.0.0.1:3000",
#     'http://localhost:8000',
#     "http://127.0.0.1:8000",
# ]
CSRF_TRUSTED_ORIGINS = ["http://localhost:3000"]
ALLOWED_HOSTS = ['127.0.0.1', '.mydomain.com','localhost','sanjeevpratap99209920.pythonanywhere.com']
CORS_ORIGIN_WHITELIST=[
    "http://localhost:3000",
    "http://127.0.0.1:8000",
]

# CORS_ALLOW_ORIGINS = [
#     'http://localhost:3000',
# ]


CORS_ALLOWED_ORIGINS = [
    'http://localhost:3000',
    'https://localhost:3000',
]









CORS_ALLOW_CREDENTIALS = True

ROOT_URLCONF = 'tweetme.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, "templates")],
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

SESSION_ENGINE = 'django.contrib.sessions.backends.db'
ASGI_APPLICATION = 'tweetme.asgi.application'
# WSGI_APPLICATION = 'tweetme.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
# DATABASES = {
#       'default': {
#           'ENGINE': 'djongo',
#           'NAME': 'TWEETME',
#     }
# }

# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

AUTH_USER_MODEL = 'twapp.CustomUser'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = 'static/'
STATICFILES_DIRS=[
        os.path.join(BASE_DIR,"static"),
]
STATIC_ROOT=os.path.join(BASE_DIR,"static-root")

# settings.py

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# REACT_APP_DIR = os.path.join(BASE_DIR, 'myapp/build')

# # Update STATICFILES_DIRS to include the REACT_APP_DIR
# STATICFILES_DIRS = [REACT_APP_DIR]

# CORS_ORIGIN_ALLOW_ALL = True              #any website has access to my api
CORS_URLS_REGEX = r"^/api/.*$"

CORS_ALLOW_HEADERS = [
    "accept",
    "accept-encoding",
    "authorization",
    "content-type",
    "dnt",
    "origin",
    "user-agent",
    "x-csrftoken",
    "x-requested-with",
]
DEFAULT_RENDERER_CLASSES=[

        'rest_framework.renderers.JSONRenderer',
      
    ]
DEFAULT_AUTHENTICATION_CLASSES=[
    'rest_framework.authentication.SessionAuthentication',
    #  'rest_framework.permissions.AllowAny',
]
if DEBUG:
    DEFAULT_RENDERER_CLASSES +=[
          'rest_framework.renderers.BrowsableAPIRenderer',

    ]
    # DEFAULT_AUTHENTICATION_CLASSES+=[
    #     'tweetme.rest_api.dev.DevAuthentication'
    # ]
    

REST_FRAMEWORK={
    "DEFAULT_AUTHENTICATION_CLASSES": DEFAULT_AUTHENTICATION_CLASSES,
    "DEFAULT_RENDERER_CLASSES":DEFAULT_RENDERER_CLASSES
}

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [("localhost", 6379)],
        },
    },
}