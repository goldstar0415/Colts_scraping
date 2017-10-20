import os
from configurations import Configuration


class Base(Configuration):
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    LOGIN_URL = '/login/'
    LOGIN_REDIRECT_URL = '/accounts/profile/'

    SECRET_KEY = '4kzg_o-hd(ejay#2i+*d822@@)&2@7-38041wem%=asx2&n$6k'

    INSTALLED_APPS = [
        'jet',
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'django.contrib.gis',
        'social_parsing',
        'accounts',
        'hashtags',
        'proxies',
        'user_account',
        'hashtag_network',
        'widget_tweaks',
    ]

    MIDDLEWARE = [
        'django.middleware.security.SecurityMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
    ]

    ROOT_URLCONF = 's_net_parsing.urls'

    TEMPLATES = [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [],
            'APP_DIRS': True,
            'OPTIONS': {
                'context_processors': [
                    'django.template.context_processors.debug',
                    'django.template.context_processors.request',
                    'django.contrib.auth.context_processors.auth',
                    'django.contrib.messages.context_processors.messages',
                ],
            },
        },
    ]

    WSGI_APPLICATION = 's_net_parsing.wsgi.application'

    # Password validation

    AUTH_PASSWORD_VALIDATORS = [
        {
            'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
        },
        {
            'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        },
        {
            'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
        },
        {
            'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
        },
    ]

    # Internationalization

    LANGUAGE_CODE = 'en-us-ru'

    TIME_ZONE = 'UTC'

    USE_I18N = True

    USE_L10N = True

    USE_TZ = True

    #  Static files
    PROJECT_ROOT = os.path.join(os.path.dirname(__file__), '..')
    SITE_ROOT = PROJECT_ROOT

    MEDIA_ROOT = os.path.join(SITE_ROOT, '../media')
    MEDIA_URL = '/media/'

    STATIC_ROOT = os.path.join(BASE_DIR, '../staticfiles')
    STATIC_URL = '/static/'

    STATICFILES_DIRS = (
        os.path.join(BASE_DIR, 'static'),
    )

    TOP_POSTS_LIKES_LIMIT = 5
    TOP_POSTS_SHARES_LIMIT = 5
    TOP_MOST_RECENT_POSTS_LIMIT = 5


class LocalDevPostgresDocker(Base):
    DEBUG = True
    ALLOWED_HOSTS = ['*']

    @property
    def DATABASES(self):
        return {'default': {
                'ENGINE': 'django.db.backends.postgresql_psycopg2',
                'NAME': 'postgres',
                'USER': 'postgres',
                'HOST': 'db',
                'PORT': 5432, }
                }

    MONGO_URL = os.getenv('MONGO_URL', 'mongodb://parseadmin:Gz=VrZX6#56n@34.212.65.19:27017/parsing')
    POSTS_COLLECTION_NAME = 'social_parsing_post'
    AUTHORS_COLLECTION_NAME = 'social_parsing_author'


class LocalDevPostgres(Base):
    DEBUG = True
    ALLOWED_HOSTS = ['*']

    @property
    def DATABASES(self):
        return {'default': {
                'ENGINE': 'django.db.backends.postgresql_psycopg2',
                'NAME': 'parseadmin',
                'USER': 'parseadmin',
                'PASSWORD': 'Fu7ELhGzV-X6!Tx',
                'HOST': '34.212.65.19',
                'PORT': '', }
                }

    MONGO_URL = os.getenv('MONGO_URL', 'mongodb://parseadmin:Gz=VrZX6#56n@34.212.65.19:27017/parsing')
    POSTS_COLLECTION_NAME = 'social_parsing_post'
    AUTHORS_COLLECTION_NAME = 'social_parsing_author'


class Prod(Base):
    DEBUG = False
    ALLOWED_HOSTS = ['*']

    @property
    def DATABASES(self):
        return {'default': {
                'ENGINE': 'django.db.backends.postgresql_psycopg2',
                'NAME': 'parseadmin',
                'USER': 'parseadmin',
                'PASSWORD': 'Fu7ELhGzV-X6!Tx',
                'HOST': '34.212.65.19',
                'PORT': '', }
                }

    MONGO_URL = os.getenv('MONGO_URL', 'mongodb://parseadmin:Gz=VrZX6#56n@34.212.65.19:27017/parsing')
    POSTS_COLLECTION_NAME = 'social_parsing_post'
    AUTHORS_COLLECTION_NAME = 'social_parsing_author'

    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'handlers': {
            'file': {
                'level': 'WARNING',
                'class': 'logging.FileHandler',
                'filename': '/opt/app/error.log',
            },
        },
        'loggers': {
            'django': {
                'handlers': ['file'],
                'level': 'WARNING',
                'propagate': True,
            },
        },
    }
