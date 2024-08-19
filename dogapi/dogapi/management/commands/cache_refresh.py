from django.core.management.base import BaseCommand, CommandError
from django.test.client import RequestFactory

from dogapi.views_api import get_repositories_status


class Command(BaseCommand):
    help = 'Refresh repository status cache'

    def handle(self, *args, **options):
        factory = RequestFactory()
        path = 'api/repostatus/'
        request = factory.get(path)
        get_repositories_status(request)
        self.stdout.write('Repository status refreshed')
