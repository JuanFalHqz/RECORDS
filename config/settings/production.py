from .base import *

# Se debe cargar desde una variable de entorno
SECRET_KEY = 'django-insecure-3fje7hx(gvho3@5k8-1m-$li@cw$e6!*bg5d5ua_jo*_e_q6_f'

DEBUG = False

# Se debe cargar desde una variable de entorno
ALLOWED_HOSTS = []

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'