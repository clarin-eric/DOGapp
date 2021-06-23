import DOG_apps.DOG_API
from django.apps import AppConfig


class API_Conf(AppConfig):
    name = DOG_apps.DOG_API.__name__
    verbose_name = 'DOG API module'


