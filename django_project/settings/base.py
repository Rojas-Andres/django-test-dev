import os
from datetime import timedelta
from os import environ, getenv
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(".env", verbose=True)

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("SECRET_KEY", "SECRET_KEY")
ENVIRONMENT = os.getenv("ENVIRONMENT", "dev")
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Application definition

BASE_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
]

LOCAL_APPS = [
    "django_apps.core",
    "django_apps.user",
]

THIRD_APPS = [
    "corsheaders",
    "rest_framework",
    "rest_framework.authtoken",
    "dj_rest_auth",
    "dj_rest_auth.registration",
    "anymail",  # TODO: Review if you use sendgrid
    "django_filters",
    "simple_history",
    "drf_yasg",
    "rest_framework_simplejwt",
    "rest_framework_simplejwt.token_blacklist",
]
SITE_ID = 1

INSTALLED_APPS = BASE_APPS + LOCAL_APPS + THIRD_APPS


MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "simple_history.middleware.HistoryRequestMiddleware",
]

ROOT_URLCONF = "django_project.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "django_project.wsgi.application"

SWAGGER_LOGIN_URL = "/admin/authentication/token"
# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

# AUTH_PASSWORD_VALIDATORS = [
#     {
#         "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
#     },
#     {
#         "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
#     },
#     {
#         "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
#     },
#     {
#         "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
#     },
# ]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


STATIC_URL = "static/"


DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

REST_FRAMEWORK = {
    "DEFAULT_SCHEMA_CLASS": "rest_framework.schemas.coreapi.AutoSchema",
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.SessionAuthentication",
    ],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.LimitOffsetPagination",
    "DEFAULT_FILTER_BACKENDS": ["django_filters.rest_framework.DjangoFilterBackend"],
}

SWAGGER_SETTINGS = {
    "USE_SESSION_AUTH": True,
    "api_version": "latest",
    "LOGIN_URL": SWAGGER_LOGIN_URL,
    "DEFAULT_PARSER_CLASSES": [
        "rest_framework.parsers.FormParser",
        "rest_framework.parsers.MultiPartParser",
        "rest_framework.parsers.JSONParser",
    ],
    "JSON_EDITOR": True,
    "SHOW_REQUEST_HEADERS": True,
    "SECURITY_DEFINITIONS": {
        "Bearer": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header",
        }
    },
    "SUPPORTED_SUBMIT_METHODS": ["get", "post", "put", "delete", "patch"],
    "DEFAULT_GENERATOR_CLASS": "rest_framework.schemas.generators.BaseSchemaGenerator",
}


# Authentification with dj_rest_auth and simple_jwt
AUTH_USER_MODEL = "user.User"
SITE_ID = 1


# Email with sendgrid and anymail
EMAIL_BACKEND = "anymail.backends.sendgrid.EmailBackend"

ACCOUNT_AUTHENTICATION_METHOD = "email"
AUTHENTICATION_METHOD = "email"
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_USERNAME_REQUIRED = False
ANYMAIL = {
    "SENDGRID_API_KEY": os.getenv("SENDGRID_API_KEY", "SENDGRID_API_KEY"),
}


# SMS with twilio
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID", "TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN", "TWILIO_AUTH_TOKEN")
TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER", "TWILIO_PHONE_NUMBER")

AWS_REGION_NAME = os.environ.get("AWS_REGION_NAME")
AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")
REDIS_HOSTNAME = getenv("REDIS_HOSTNAME", "redis")
REDIS_PORT = int(getenv("REDIS_PORT", 6379))

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": f"redis://{REDIS_HOSTNAME}:{REDIS_PORT}/0",
    }
}

CACHEOPS_ENABLED = bool(int(getenv("CACHEOPS_ENABLED", "1")))

CACHEOPS_REDIS = f"redis://{REDIS_HOSTNAME}:{REDIS_PORT}/0"

DEFAULT_PAGE_SIZE = 10
