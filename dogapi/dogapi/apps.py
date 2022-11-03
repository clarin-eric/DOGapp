import dogapi
from django.apps import AppConfig


class DogApiConf(AppConfig):
    name = dogapi.__name__
    verbose_name = 'DOG API module'


