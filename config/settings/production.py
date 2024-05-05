from .base import *
from decouple import config, Csv

SECRET_KEY = 'django-insecure-3fje7hx(gvho3@5k8-1m-$li@cw$e6!*bg5d5ua_jo*_e_q6_f'

DEBUG = config('DEBUG', cast=bool)

ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=Csv())

# Database
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
# https://docs.djangoproject.com/en/4.2/howto/static-files/

# Note: Replace 'supersecure.codes' with your domain
STATIC_ROOT = "/var/www/rdmcuba.duckdns.org/static"

STATIC_URL = 'static/'

# replace HTTP request to HTTPS
SECURE_HSTS_SECONDS = 30  # Unit is seconds; *USE A SMALL VALUE FOR TESTING!*
SECURE_HSTS_PRELOAD = True
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
