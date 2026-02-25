import os
import sys
from pathlib import Path

from src.const import (
    ENV,
    LOCAL_ENV,
    NORMAL_IMAGE_EXPIRY_SECONDS,
    SERVER_HOST,
)
from src.utils.log.formatter import LogFormatter

# Flag indicating that Django is being run via manage.py (i.e., a management command
# such as migrate, collectstatic, shell, etc.). Other parts of the codebase can use
# this to adjust behavior or skip runtime-only initialization when running commands.
IS_MANAGEMENT_COMMAND = len(sys.argv) > 1 and sys.argv[0].endswith("manage.py")

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ["DJANGO_SECRET_KEY"]

DEBUG = ENV == LOCAL_ENV

if DEBUG:
    ALLOWED_HOSTS = ["*"]
else:
    ALLOWED_HOSTS = [SERVER_HOST]
    CSRF_TRUSTED_ORIGINS = [f"https://{SERVER_HOST}"]

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "src",
    "storages",
    "rest_framework",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "src.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "src" / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "src.context_processors.configure_context_processors",
            ],
        },
    },
]

WSGI_APPLICATION = "src.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    },
}

AUTHENTICATION_BACKENDS = [
    "src.auth_backends.LockableModelBackend",
]

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",  # noqa: E501
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

# LANGUAGE_CODE = 'en-us'
LANGUAGE_CODE = "vi-vn"

# TIME_ZONE = 'UTC'
TIME_ZONE = "Asia/Ho_Chi_Minh"

USE_I18N = True

USE_TZ = True

STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "assets"]
STATIC_ROOT = os.getenv("DJANGO_STATIC_ROOT", BASE_DIR / "static")

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# S3 Storage base settings
AWS_S3_ENDPOINT_URL = os.environ["AWS_S3_ENDPOINT_URL"]
AWS_S3_REGION_NAME = os.environ["AWS_DEFAULT_REGION"]
AWS_ACCESS_KEY_ID = os.environ["AWS_ACCESS_KEY_ID"]
AWS_SECRET_ACCESS_KEY = os.environ["AWS_SECRET_ACCESS_KEY"]
AWS_STORAGE_BUCKET_NAME = os.environ["AWS_STORAGE_BUCKET_NAME"]
AWS_S3_FILE_OVERWRITE = False
AWS_QUERYSTRING_EXPIRE = NORMAL_IMAGE_EXPIRY_SECONDS

STORAGES = {
    "default": {
        "BACKEND": "src.storages.storage.Storage",
        "OPTIONS": {
            "location": "images",
        },
    },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
}

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.SessionAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
    "DATETIME_FORMAT": "%d/%m/%Y %H:%M:%S",
}

LOGIN_URL = "/login/"
LOGIN_REDIRECT_URL = "/dashboard/"
LOGOUT_REDIRECT_URL = "/login/"

if DEBUG:
    CACHES = {
        "default": {
            "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        },
    }
else:
    CACHES = {
        "default": {
            "BACKEND": "django.core.cache.backends.redis.RedisCache",
            "LOCATION": "redis://127.0.0.1:6379",
        },
    }

LOGIN_LOCK_MAX_FAILED_ATTEMPTS = 5
LOGIN_LOCK_RETRY_AFTER_SECONDS = 300
LOGIN_FAIL_KEY_PREFIX = "auth:fail:"
LOGIN_LOCK_KEY_PREFIX = "auth:lock:"

Path("logs").mkdir(parents=True, exist_ok=True)

LOGGING = (
    {
        "version": 1,
        "disable_existing_loggers": True,
        "formatters": {
            "file": {
                "()": LogFormatter,
            },
            "standard": {
                "format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s",
            },
        },
        "handlers": {
            "file": {
                "level": "INFO",
                "class": "src.utils.log.handler.S3ConcurrentTimedRotatingFileHandler",
                "filename": "logs/general.log",
                "when": "M",
                "interval": 5,
                "backupCount": 12,
                "formatter": "file",
                "encoding": "utf8",
                "delay": False,
                "mode": "a",
            },
            "console": {
                "level": "DEBUG",
                "class": "logging.StreamHandler",
                "formatter": "standard",
            },
        },
        "loggers": {
            "django": {
                "handlers": ["file", "console"] if not DEBUG else ["console"],
                "level": "INFO",
                "propagate": False,
            },
            "boto3": {
                "handlers": ["file", "console"] if not DEBUG else ["console"],
                "level": "INFO",
                "propagate": False,
            },
            "botocore": {
                "handlers": ["file", "console"] if not DEBUG else ["console"],
                "level": "INFO",
                "propagate": False,
            },
            "": {
                "handlers": ["file", "console"] if not DEBUG else ["console"],
                "level": "INFO" if not DEBUG else "DEBUG",
            },
        },
    }
    if not IS_MANAGEMENT_COMMAND
    else {}
)
