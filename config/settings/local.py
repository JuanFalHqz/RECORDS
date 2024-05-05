from .base import *
from decouple import config, Csv

SECRET_KEY = 'django-insecure-3fje7hx(gvho3@5k8-1m-$li@cw$e6!*bg5d5ua_jo*_e_q6_f'

DEBUG = config('DEBUG', cast=bool)

ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=Csv())

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

"""DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}"""
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST'),  # O la dirección de tu servidor de base de datos
        'PORT': config('DB_PORT'),  # Por lo general, el puerto predeterminado es 5432
    }
}
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'
