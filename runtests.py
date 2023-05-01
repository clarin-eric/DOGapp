import sys

from debug_toolbar.panels.logging import collector
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
        ],
        MIDDLEWARE=[
            'debug_toolbar.middleware.DebugToolbarMiddleware',
        ],
        LOGGING={
            'version': 1,
            'handlers': {
                # existing handlers
                'djdt_log': {
                    'level': 'DEBUG',
                    'class': 'debug_toolbar.panels.logging.ThreadTrackingHandler',
                    'collector': collector,
                },
                'console': {
                    'level': 'DEBUG',
                    'class': 'logging.StreamHandler'
                }
            },
            'root': {
                'level': 'DEBUG',
                'handlers': ['djdt_log', 'console'],
            },
            'loggers': {
                '': {
                    'level': 'DEBUG',
                    'handlers': ['console'],
                }
            }
        },
        API_NETLOC="http://127.0.0.1:8000/api"
    )
    django.setup()
    TestRunner = get_runner(settings)
    test_runner = TestRunner()
    failures = test_runner.run_tests(["dogapi.tests"])
    sys.exit(bool(failures))
