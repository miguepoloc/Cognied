from .base import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-h82t0qs_s_&fop)=lw8@k$+d)x0i%)'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]
INTERNAL_IPS = [
    '127.0.0.1',
    'localhost',
    '0.0.0.0'
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'kidsbpep',
        'USER': 'kidsbpep',
        'PASSWORD': 'Da_X0HObSCVPd9uHyG9RA--JVubROEar',
        'HOST': 'kashin.db.elephantsql.com',
        'PORT': '5432',
    }
}
