from django.conf import settings
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.template import RequestContext
import logging.config


import requests

from .utils import TaxonomyTree
from .forms import MIMETypeForm

logging.config.dictConfig(settings.LOGGING)

API_NETLOC = settings.API_NETLOC
DTR_ENABLED = settings.DTR_ENABLED
VERIFY_SSL = settings.VERIFY_SSL


def dtr(request: HttpRequest) -> HttpResponse:
    context: RequestContext = RequestContext(request)
    mimetype_form: MIMETypeForm = MIMETypeForm(request.GET, use_required_attribute=False)

    context.push({"view": "dtr"})
    context.push({"DTR_ENABLED": DTR_ENABLED})

    if mimetype_form.is_valid():
        context.push({"mimetype_form": mimetype_form})
        mimetypes = mimetype_form.cleaned_data['mimetype_field']

        api_url = API_NETLOC + f'/expanddatatype/?mimetype={",".join(mimetypes)}'

        api_response = requests.get(api_url, verify=VERIFY_SSL)

        print(api_response.json())
        context.push({f"taxonomies": api_response.json()})
        return render(request, f"UI/_expanddatatype.html", context.flatten())
    else:
        context.push({"mimetype_form": mimetype_form})
        context.push({"view": "dtr"})
        return render(request, "UI/_dtr.html", context.flatten())
