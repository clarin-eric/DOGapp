from django.apps import AppConfig

from DOG_apps import dog_api

class DogApiConf(AppConfig):
    name = dog_api.__name__
    verbose_name = 'DOG API module'


