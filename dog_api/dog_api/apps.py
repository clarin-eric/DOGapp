import dog_api
from django.apps import AppConfig


class DogApiConf(AppConfig):
    name = dog_api.__name__
    verbose_name = 'DOG API module'


