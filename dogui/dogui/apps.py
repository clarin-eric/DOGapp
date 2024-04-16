import dogui
from django.apps import AppConfig


class DogUIConf(AppConfig):
    name = dogui.__name__
    verbose_name = 'DOG UI module'
