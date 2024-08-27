from pathlib import Path
import os
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

# Define the base directory of the project
BASE_DIR = Path(__file__).resolve().parent.parent

# Secret key for the project, retrieved from environment variables
SECRET_KEY = os.environ.get("SECRET_KEY")

# Toggle debug mode based on environment settings
DEBUG = os.environ.get("DEBUG")

# Hosts allowed to access this Django application
ALLOWED_HOSTS = []

# Application definition
INSTALLED_APPS = [
    # Django default apps
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Third-party apps
    "drf_spectacular",  # For API schema generation
    "rest_framework",  # Django REST Framework for building APIs
    # Your apps
    "server.apps.ServerConfig",  # Configuration for the 'server' app
    "account.apps.AccountConfig",  # Configuration for the 'account' app
]

# Middleware configuration
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# Root URL configuration
ROOT_URLCONF = "DjChat.urls"

# Template engine configuration
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],  # Directories to search for templates
        "APP_DIRS": True,  # Enable auto-loading of templates from apps
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

# WSGI application entry point for production
WSGI_APPLICATION = "DjChat.wsgi.application"

# Database configuration using SQLite
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# Password validation settings
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

# Internationalization settings
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True  # Enable Django's translation system
USE_TZ = True  # Enable timezone support

# Static files configuration
STATIC_URL = "static/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")
MEDIA_URL = "media/"

# Set the default primary key field type
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Custom user model configuration
AUTH_USER_MODEL = "account.Account"

# Django REST Framework settings
REST_FRAMEWORK = {
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",  # OpenAPI schema generator
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.SessionAuthentication",  # Session-based authentication
    ],
}

# drf-spectacular settings for generating API documentation
SPECTACULAR_SETTINGS = {
    "TITLE": "Your Project API",  # API title
    "DESCRIPTION": "Your project description",  # API description
    "VERSION": "1.0.0",  # API version
    "SERVE_INCLUDE_SCHEMA": False,  # Exclude schema from being served
}
