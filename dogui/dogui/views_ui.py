from django.conf import settings
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.template import RequestContext
import logging.config
import requests

from .forms import PIDForm

logging.config.dictConfig(settings.LOGGING)
API_NETLOC = settings.API_NETLOC


def home(request: HttpRequest) -> HttpResponse:
    context: RequestContext = RequestContext(request)
    pid_form: PIDForm() = PIDForm(request.GET)
    if pid_form.is_valid():
        context.push({"pid_form": pid_form})
        functionality = pid_form.cleaned_data['functionality_field']
        pids = pid_form.cleaned_data['pid_field']
        api_url = API_NETLOC + f'/{functionality}/?pid={",".join(pids)}'
        api_response = requests.get(api_url, verify=settings.VERIFY_SSL)
        logging.critical(api_response)
        context.push({f"{functionality}_response": api_response.json()})

        return render(request, f"UI/_{functionality}.html", context.flatten())
    else:
        pid_form: PIDForm = PIDForm(initial={'functionality_field': 'sniff'})
        context.push({"pid_form": pid_form})
        return render(request, "UI/_home.html", context.flatten())
