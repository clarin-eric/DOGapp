"""
Django settings for DOG-apps project.

Generated by 'django-admin startproject' using Django 4.0.3

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""

from os.path import abspath, dirname, join

from dog_project import __name__ as app_name

BASE_DIR = dirname(dirname(__file__))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY ='testsecret087B*#bAIUSd'
## Secure cookies have to be turned off in development mode, assuming there is
## no reverse proxy with X-Forwarded-Proto=https or https://tools.ietf.org/html/rfc7239.
DEBUG = True # TODO: templatize
SESSION_COOKIE_SECURE = not DEBUG
SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_SECURE = not DEBUG
CSRF_COOKIE_HTTPONLY = True
PIWIK_WEBSITE_ID = "1000"
PROJECT_DIR = abspath(dirname(__file__))
ALLOWED_HOSTS = ['127.0.0.1', 'localhost', 'django']
TEMPLATE_DEBUG = DEBUG
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
MEDIA_ROOT = ''
STATIC_URL = '/static/'
STATIC_ROOT = join(PROJECT_DIR,
                   '../../dog_apps/dog_api/assets')
STATICFILES_DIRS = (join(BASE_DIR, 'DOGapp/static'))

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)
ROOT_URLCONF = app_name + '.urls'

TEMPLATE_LOADERS = ('django.template.loaders.app_directories.Loader', )
# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'dog_api.apps.DogApiConf',
    'doglib',
    'drf_yasg',
    'rest_framework',
    'rest_framework_swagger',
]

REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ],
}

REDOC_SETTINGS = {
    'LAZY_RENDERING': False,
}

SWAGGER_SETTINGS = {
    'DEFAULT_GENERATOR_CLASS': 'drf_yasg.generators.OpenAPISchemaGenerator',
    'DEFAULT_AUTO_SCHEMA_CLASS': 'drf_yasg.inspectors.SwaggerAutoSchema',
    'SECURITY_DEFINITIONS': {
        'basic': {
            'type': 'basic'
        }
    },
    'DEFAULT_INFO': app_name + '.urls.openapi_info',
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

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


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/Amsterdam'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


CORS_ORIGIN_ALLOW_ALL = True

# TODO
# CORS_ORIGIN_WHITELIST = (
#   'http://localhost:8000',
# )