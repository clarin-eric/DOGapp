from django.core.cache import cache
from django.core.management.base import BaseCommand, CommandError
from django.test.client import RequestFactory

from dogapi.models import dog


class Command(BaseCommand):
    help = 'Refresh repository status cache'

    def handle(self, *args, **options):
        repositories_status = dog.get_all_repositories_status()
        cache.set('repositories_status', repositories_status, 86400)
        self.stdout.write('Repository status refreshed')
