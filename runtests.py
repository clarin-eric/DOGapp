import sys
import django
from django.conf import settings
from django.test.utils import get_runner


if __name__ == "__main__":
    settings.configure(
        DEBUG=True,
        USE_TZ=True,
        REST_FRAMEWORK={
            'DEFAULT_RENDERER_CLASSES': [
                'rest_framework.renderers.JSONRenderer',
                'rest_framework.renderers.BrowsableAPIRenderer',
            ],
        },
        ROOT_URLCONF="dogproject" + '.urls',
        INSTALLED_APPS=[
            "debug_toolbar",
            "django.contrib.auth",
            "django.contrib.contenttypes",
            "django.contrib.sites",
            "dogapi",
            "dogui",
        ],
        MIDDLEWARE=[
            'debug_toolbar.middleware.DebugToolbarMiddleware',
        ],
        LOGGING={
            'version': 1,
            'handlers': {
                # existing handlers
                'console': {
                    'level': 'DEBUG',
                    'class': 'logging.StreamHandler'
                }
            },
            'root': {
                'level': 'DEBUG',
                'handlers': ['console'],
            },
            'loggers': {
                '': {
                    'level': 'DEBUG',
                    'handlers': ['console'],
                }
            }
        },
        API_NETLOC="http://127.0.0.1:8000/api",
        TEMPLATE_LOADERS=[
            'django.template.loaders.app_directories.Loader',
        ],
        TEMPLATES=[
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
    )
    django.setup()
    TestRunner = get_runner(settings)
    test_runner = TestRunner(verbosity=2)
    failures = test_runner.run_tests(["dogapi.tests"])
    sys.exit(failures)
