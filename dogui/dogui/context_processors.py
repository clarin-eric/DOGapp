from django.conf import settings


def version(request):
    # pylint: disable=unused-argument
    return {'VERSION': settings.VERSION}
