import dogproject
from django.apps import AppConfig


class DogProjectConf(AppConfig):
    name = dogproject.__name__
    verbose_name = 'DOG API module'


