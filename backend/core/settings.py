from pathlib import Path
import os
import environ

env = environ.Env()
environ.Env.read_env(os.path.join(Path(__file__).resolve().parent.parent.parent, '.env'))

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY', default='django-insecure-fallback-key-for-dev-only')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool('DEBUG', default=False)

raw_hosts = env.str('ALLOWED_HOSTS', default='*')
ALLOWED_HOSTS = [host.strip() for host in raw_hosts.split(',')] if raw_hosts else ['*']

raw_origins = env.str('CSRF_TRUSTED_ORIGINS', default='')
CSRF_TRUSTED_ORIGINS = [origin.strip() for origin in raw_origins.split(',')] if raw_origins else []

# Render proxy sozlamalari
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')


# Application definition

INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites', # allauth requires this

    # allauth apps
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    
    # Providers
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.github',
    'allauth.socialaccount.providers.telegram',

    'accounts',
    'posts',
    'chat',
]

SITE_ID = 1

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    
    # allauth middleware
    'allauth.account.middleware.AccountMiddleware',

    # MANA SHU QATOR BORLIGINI VA TO'G'RI YOZILGANINI TEKSHIRING:
    'posts.middleware.OwnerPostRestrictionMiddleware',
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'], # <-- SHU QATORGA E'TIBOR BERING
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'chat.context_processors.unread_messages_count',
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': env.db('DATABASE_URL'),
}


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = []


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'uz'
TIME_ZONE = 'Asia/Tashkent'
USE_I18N = True
USE_L10N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
# CompressedStaticFilesStorage - .map fayllarni tekshirmaydi
STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'accounts.User'



JAZZMIN_SETTINGS = {
    "site_title": "Anonym Space Admin",
    "site_header": "Anonym Space",
    "welcome_sign": "Anonym Space boshqaruv paneliga xush kelibsiz",
    "search_model": ["accounts.User", "posts.Post"],
    "topmenu_links": [
        {"name": "Bosh sahifa", "url": "admin:index", "permissions": ["auth.view_user"]},
        {"name": "Saytga o'tish", "url": "/", "new_window": True},
    ],
    "show_sidebar": True,
    "navigation_expanded": True,
    "theme": "darkly", # Bu siz xohlagan Dark mode uchun
}

PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.Argon2PasswordHasher',
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
]


# Login qilgandan keyin qayerga o'tsin (Asosiy sahifaga)
LOGIN_REDIRECT_URL = 'home'

# Logout qilgandan keyin qayerga o'tsin
LOGOUT_REDIRECT_URL = 'login'

# Allauth xususiy sozlamalari
ACCOUNT_USER_MODEL_USERNAME_FIELD = 'nickname'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = 'email'
SOCIALACCOUNT_AUTO_SIGNUP = True
SOCIALACCOUNT_LOGIN_ON_GET = True
ACCOUNT_DEFAULT_HTTP_PROTOCOL = 'https'

# Ijtimoiy tarmoqlar provayderlari
SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'APP': {
            'client_id': env('GOOGLE_CLIENT_ID', default=''),
            'secret': env('GOOGLE_CLIENT_SECRET', default=''),
            'key': ''
        },
        'SCOPE': [
            'profile',
            'email',
        ],
        'AUTH_PARAMS': {
            'access_type': 'online',
        }
    },
    'github': {
        'APP': {
            'client_id': env('GITHUB_CLIENT_ID', default=''),
            'secret': env('GITHUB_CLIENT_SECRET', default=''),
            'key': ''
        }
    },
    'telegram': {
        'APP': {
            'client_id': env('TELEGRAM_BOT_TOKEN', default=''),
            'secret': env('TELEGRAM_BOT_TOKEN', default=''),
        }
    }
}
# Logging configuration to see errors in Render logs
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'ERROR',
            'propagate': True,
        },
    },
}
