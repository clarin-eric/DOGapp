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
    context: RequestContext = RequestContext(request)
    pid_form: PIDForm() = PIDForm(request.GET)
    logger.debug(f"{pid_form.is_valid()}")
    if pid_form.is_valid():
        context.push({"pid_form": pid_form})
        functionality = pid_form.cleaned_data['functionality_field']
        pids = pid_form.cleaned_data['pid_field']
        logger.debug(f'{pids}')
        api_url = 'http://' + API_NETLOC + f'/{functionality}/?pid={",".join(pids)}'
        logger.debug(api_url)

        api_response = requests.get(api_url)
        logger.debug(f'{api_response}')
        context.push({f"{functionality}_response": api_response.json()})

        return render(request, f"UI/_{functionality}.html", context.flatten())
    else:
        pid_form: PIDForm = PIDForm(initial={'functionality_field': 'sniff'})
        context.push({"pid_form": pid_form})
        return render(request, "UI/_home.html", context.flatten())
