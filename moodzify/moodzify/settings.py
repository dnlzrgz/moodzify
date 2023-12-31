"""
Django settings for moodzify project.
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path

from environs import Env

# Environment variables
# https://github.com/sloria/environs
env = Env()
env.read_env()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Secret key
# https://docs.djangoproject.com/en/4.2/topics/signing/
SECRET_KEY = env.str(
    "DJANGO_SECRET_KEY",
    "django-insecure-6w9k#_p%g3032jh*t-79bqxkda#99sms^fyf9+*@^mo7lso6v7",
)

# Debug mode
# https://docs.djangoproject.com/en/4.2/ref/settings/#std-setting-DEBUG
DEBUG = env.bool("DEBUG", False)

ALLOWED_HOSTS = []

INTERNAL_IPS = [
    "127.0.0.1",
]

if DEBUG:
    import socket

    hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())
    INTERNAL_IPS = [ip[: ip.rfind(".")] + ".1" for ip in ips] + [
        "127.0.0.1",
        "10.0.2.2",
    ]

# Application definition

INSTALLED_APPS = [
    # Django
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    # Static files
    "whitenoise.runserver_nostatic",
    "django.contrib.staticfiles",
    # 3rd party
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    # Local
    "accounts",
    "moods",
]

if DEBUG:
    INSTALLED_APPS += ["debug_toolbar"]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "allauth.account.middleware.AccountMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

if DEBUG:
    middleware_idx = MIDDLEWARE.index("django.middleware.common.CommonMiddleware") + 1
    MIDDLEWARE.insert(
        middleware_idx,
        "debug_toolbar.middleware.DebugToolbarMiddleware",
    )

ROOT_URLCONF = "moodzify.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            BASE_DIR / "templates",
        ],
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

WSGI_APPLICATION = "moodzify.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

POSTGRES_NAME = env.str("POSTGRES_NAME", "")
POSTGRES_USER = env.str("POSTGRES_USER", "")
POSTGRES_PASSWORD = env.str("POSTGRES_PASSWORD", "")
POSTGRES_HOST = env.str("POSTGRES_HOST", "")

if all([POSTGRES_NAME, POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_HOST]):
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": POSTGRES_NAME,
            "USER": POSTGRES_USER,
            "PASSWORD": POSTGRES_PASSWORD,
            "HOST": POSTGRES_HOST,
            "PORT": env.int("POSTGRES_PORT", 5432),
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

# Storage
# https://docs.djangoproject.com/en/4.2/ref/files/storage/

STORAGES = {
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_ROOT = BASE_DIR / "staticfiles"

STATIC_URL = "static/"

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Email backend
# https://docs.djangoproject.com/en/4.2/ref/settings/#email-backend

EMAIL_HOST = env("EMAIL_HOST", default="mailpit")
EMAIL_PORT = 1025
EMAIL_BACKEND = env(
    "DJANGO_EMAIL_BACKEND",
    default="django.core.mail.backends.smtp.EmailBackend",
)

EMAIL_TIMEOUT = 5

# Custom authentication
# https://docs.djangoproject.com/en/4.2/topics/auth/customizing/

AUTH_USER_MODEL = "accounts.CustomUser"

LOGIN_REDIRECT_URL = "home"
LOGOUT_REDIRECT_URL = "home"

# All-auth
# https://allauth.org/

AUTHENTICATION_BACKENDS = (
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
)

SITE_ID = 1

ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_SIGNUP_PASSWORD_ENTER_TWICE = True
ACCOUNT_SESSION_REMEMBER = True
ACCOUNT_AUTHENTICATION_METHOD = "email"
ACCOUNT_UNIQUE_EMAIL = True
