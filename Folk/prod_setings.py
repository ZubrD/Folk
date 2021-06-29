import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


SECRET_KEY = '(t9n#=65iba)4)2n^d9pc&24rfh3hsakeoq@wp#ovo@7goek+&^q@o88jvk=1hw'

DEBUG = False

ALLOWED_HOSTS = ['127.0.0.1']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'forseti_db',
        'USER': 'forseti_admin',
        'PASSWORD': 'forseti_12345',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

STATIC_DIR = os.path.join(BASE_DIR, 'static')
STATICFILES_DIRS = [STATIC_DIR]
STATIC_ROOT = os.path(BASE_DIR, 'static')