import os
import environ
from pathlib import Path

# Initialise environment variables
env = environ.Env()
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent
# Take environment variables from .env file
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

DATABASES = {
    'default': {
        'ENGINE': env("DATABASE_ENGINE", default=""),
        'NAME': env("DATABASE_NAME", default=""),
        'USER': env("DATABASE_USER", default=""),
        'PASSWORD': env("DATABASE_PASSWORD", default=""),
        'HOST': env("DATABASE_HOST", default=""),
        'PORT': env("DATABASE_PORT", default="")
    }
}

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = env("EMAIL_HOST_USER", default="")
EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD", default="")
EMAIL_PORT = 587
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

BASE_URL = env("BASE_URL", default="")
