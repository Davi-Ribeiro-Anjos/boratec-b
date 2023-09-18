import os
from datetime import timedelta
from pathlib import Path

from corsheaders.defaults import default_headers

from dotenv import load_dotenv

load_dotenv()


BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get("SECRET_KEY")

dev = False

if dev:
    DEBUG = True

    ALLOWED_HOSTS = ["localhost", "127.0.0.1", "[::1]", "back.bora.tec.br"]

    CORS_ALLOWED_ORIGINS = ["http://localhost:5173"]

    CSRF_TRUSTED_ORIGINS = ["http://localhost:5173"]

    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
        }
    }

else:
    DEBUG = True

    ALLOWED_HOSTS = [
        "127.0.0.1",
        "back.bora.tec.br",
        "www.back.bora.tec.br",
    ]

    CORS_ALLOWED_ORIGINS = [
        "http://back.bora.tec.br",
        "https://back.bora.tec.br",
        "http://www.back.bora.tec.br",
        "https://www.back.bora.tec.br",
    ]

    CSRF_TRUSTED_ORIGINS = [
        "http://back.bora.tec.br",
        "https://back.bora.tec.br",
        "http://www.back.bora.tec.br",
        "https://www.back.bora.tec.br",
    ]

    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True

    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.mysql",
            "NAME": os.environ.get("DB_NAME"),
            "USER": os.environ.get("DB_USER"),
            "PASSWORD": os.environ.get("DB_PASS"),
            "HOST": os.environ.get("DB_HOST"),
            "PORT": "3306",
        }
    }

CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_HEADERS = list(default_headers) + [
    "x-xsrf-token",
    "access-control-allow-headers",
    "access-control-allow-origin",
    "access-control-allow-methods",
]

CORS_ALLOW_METHODS = [
    "GET",
    "OPTIONS",
    "PATCH",
    "POST",
]

THIRD_PARTY_APPS = [
    "corsheaders",
    "rest_framework",
    "rest_framework_simplejwt",
]

MY_APPS = [
    "branches",
    "clients",
    "deliveries_histories",
    "employees",
    "employees_dismissals",
    "employees_epis",
    "epis_carts",
    "epis_groups",
    "epis_items",
    "epis_requests",
    "epis_sizes",
    "fleets_availabilities",
    "pallets_controls",
    "pallets_movements",
    "payments_histories",
    "pj_complements",
    "purchases_entries",
    "purchases_requests",
    "vehicles",
]

DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

INSTALLED_APPS = MY_APPS + DJANGO_APPS + THIRD_PARTY_APPS

APPEND_SLASH = False

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "_app.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
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

WSGI_APPLICATION = "_app.wsgi.application"


AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


SESSION_COOKIE_AGE = 10800


DATETIME_FORMAT = "d/m/Y H:i"
DATE_FORMAT = "d/m/Y"

LANGUAGE_CODE = "pt-br"

TIME_ZONE = "America/Sao_Paulo"

USE_I18N = True
USE_L10N = True
USE_TZ = False


STATIC_URL = os.environ.get("STATIC_URL")
STATIC_ROOT = os.environ.get("STATIC_ROOT")

MEDIA_URL = os.environ.get("MEDIA_URL")
MEDIA_ROOT = os.environ.get("MEDIA_ROOT")


EMAIL_BACKEND = os.environ.get("EMAIL_BACKEND")
EMAIL_HOST = os.environ.get("EMAIL_HOST")
EMAIL_PORT = os.environ.get("EMAIL_PORT")
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD")


DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ],
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=1),  # ,minutes=60),
    "SLIDING_TOKEN_REFRESH_LIFETIME": timedelta(days=1),
    "SLIDING_TOKEN_REFRESH_EXPIRATION": True,
    "SLIDING_TOKEN_REFRESH_DELTA": timedelta(days=1),
    "ALGORITHM": "HS256",
    "SIGNING_KEY": SECRET_KEY,
    "AUTH_HEADER_TYPES": ("Bearer",),
    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
}
