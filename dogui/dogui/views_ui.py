import django.conf
from django.conf import settings
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render
from django.template import RequestContext
import logging
import logging.config
import requests
from typing import List
from doglib.pid import pid_factory

from .forms import PIDForm

logging.config.dictConfig(settings.LOGGING)
API_NETLOC = settings.NETLOC + '/api'


def home(request: HttpRequest) -> HttpResponse:
    logger = logging.getLogger(__name__)
    # if request.method == 'POST':
    #     form = PIDForm(request.POST)
    #     if form.is_valid():
    #         return sniff_result(request, form.cleaned_data["pid"])
    #     else:
    #         print(form.errors)
    # else:
    form = PIDForm(request.GET)
    context: RequestContext = RequestContext(request)
    context.push({"form": form})
    logger.debug("BEFORE VALID")
    if form.is_valid():
        logger.debug("IS VALID")
        pids: List[str] = form.cleaned_data["pid"]
        sniff_response = requests.get('http://' + API_NETLOC + f'/sniff/?pid={",".join(pids)}')
        logger.debug(str(sniff_response))
        logger.debug(str(sniff_response.json()))
        context.push({"sniff_response": sniff_response.json()})

    return render(request, "UI/_home.html", context.flatten())


# def sniff_result(request, pid_candidate: str) -> HttpResponse:
#     response = request.GET(API_NETLOC + f'sniff/?pid={pid_candidate}')
#     context: RequestContext = RequestContext(request, response.json())
#     return render(request, "UI/_sniff_result.html", {'pid': pid_candidate})
