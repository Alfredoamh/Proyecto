from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.

BASE_DIR = Path(__file__).resolve().parent.parent

TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "wcnq$7-+50xdid0#sb)jx=lc9uwk=sc8ov@2hk$4u(ih_p9&"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["127.0.0.1", "localhost"]

# Application definition
DEFAULT_DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    'django.contrib.humanize',
]

LOCAL_APPS = [
    "SistemaApp",
    "DocumentoApp",
    "ReportsApp",
]

THIRD_APPS = [
    "tailwind",
    "theme",
    "allauth",
    "allauth.account",
    "allauth.mfa",
    "crispy_forms",
    "crispy_tailwind",
    "preventconcurrentlogins",
    "axes",
]

INSTALLED_APPS = DEFAULT_DJANGO_APPS + LOCAL_APPS + THIRD_APPS

TAILWIND_APP_NAME = "theme"

INTERNAL_IPS = [
    "127.0.0.1",
]

NPM_BIN_PATH = "C:/Program Files/nodejs/npm.cmd"

CRISPY_ALLOWED_TEMPLATE_PACKS = "tailwind"

CRISPY_TEMPLATE_PACK = "tailwind"

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "allauth.account.middleware.AccountMiddleware",
    "preventconcurrentlogins.middleware.PreventConcurrentLoginsMiddleware",
    "axes.middleware.AxesMiddleware",
]

ROOT_URLCONF = "core.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [TEMPLATES_DIR],
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

AUTHENTICATION_BACKENDS = [
    "axes.backends.AxesStandaloneBackend",
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
]

WSGI_APPLICATION = "core.wsgi.application"

MFA_ADAPTER = "allauth.mfa.adapter.DefaultMFAAdapter"

MFA_FORMS = {
    "authenticate": "allauth.mfa.forms.AuthenticateForm",
    "reauthenticate": "allauth.mfa.forms.AuthenticateForm",
    "activate_totp": "allauth.mfa.forms.ActivateTOTPForm",
    "deactivate_totp": "allauth.mfa.forms.DeactivateTOTPForm",
}

SITE_ID = 1

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "mejor_nines",
        "USER": "postgres",
        "PASSWORD": 12345,
        "HOST": "127.0.0.1",
        "PORT": 5432,
    }
}

PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.Argon2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher",
    "django.contrib.auth.hashers.BCryptSHA256PasswordHasher",
    "django.contrib.auth.hashers.ScryptPasswordHasher",
]

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
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = "es-us"

# TIME_ZONE = "UTC"
TIME_ZONE = "America/Santiago"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = "static/"

STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


if DEBUG:
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
# else: EMAIL_BACKEND = [Configuración de correo]

# AUTH_USER_MODEL = 'auth.User'

ACCOUNT_ALLOW_REGISTRATION = True

# ACCOUNT_AUTHENTICATED_LOGIN_REDIRECTS = True
ACCOUNT_AUTHENTICATED_LOGIN_REDIRECTS = False
LOGIN_REDIRECT_URL = "Home"

ACCOUNT_AUTHENTICATION_METHOD = "username_email"
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_UNIQUE_EMAIL = True

ACCOUNT_EMAIL_VERIFICATION = "mandatory"
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 3

ACCOUNT_LOGOUT_ON_GET = True

# ACCOUNT_LOGIN_ATTEMPT_LIMIT_REACHED = "para personalizar mensaje"

SESSION_COOKIE_AGE = 1200  # 20 minutes in seconds

LOGIN_URL = "account_login"

# -----------------------------------------------

MFA_RECOVERY_CODE_COUNT = 10
# El número de códigos de recuperación.

MFA_TOTP_PERIOD = 30
# El período durante el cual un código TOTP será válido, en segundos.

MFA_TOTP_DIGITS = 6
# The number of digits for TOTP codes.

# -------------------------------------------------
import datetime as dt

delta = dt.timedelta(minutes=1)

AXES_FAILURE_LIMIT = 10
AXES_COOLOFF_TIME = delta
AXES_RESET_ON_SUCCESS = False
AXES_ENABLE_ACCESS_FAILURE_LOG = False
AXES_LOCK_OUT_AT_FAILURE = False
