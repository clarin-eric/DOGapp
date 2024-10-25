from django.conf import settings
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.template import RequestContext
import logging.config
import requests
import sys

from .forms import PIDForm
from .utils import TaxonomyTree

logging.config.dictConfig(settings.LOGGING)
API_NETLOC = settings.API_NETLOC
DTR_ENABLED = settings.DTR_ENABLED


def dtr(request: HttpRequest) -> HttpResponse:
    context: RequestContext = RequestContext(request)
    context.push({"view": "dtr"})
    context.push({"DTR_ENABLED": DTR_ENABLED})
    return render(request, "UI/_dtr.html", context.flatten())
