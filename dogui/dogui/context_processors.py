from django.conf import settings


import re

def version(request):
    # pylint: disable=unused-argument
    version = settings.VERSION
    print(version)
    alpha_regex = re.compile(r"^[0-9]+\.[0-9]+\.[0-9]+(-)?(a|b|rc)[0-9]+$")
    beta_regex = re.compile(r"^[0-9]+\.[0-9]+\.[0-9]+$")
    if alpha_regex.match(version):
        return {"VERSION": version, "INSTANCE": "ALPHA"}
    elif beta_regex.match(version):
        return {'VERSION': version, "INSTANCE": "BETA"}
