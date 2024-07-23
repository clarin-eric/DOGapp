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


def home(request: HttpRequest) -> HttpResponse:
    context: RequestContext = RequestContext(request)
    pid_form: PIDForm() = PIDForm(request.GET)

    all_repo_status_url = API_NETLOC + "/repostatus/"
    all_repo_status_response = requests.get(all_repo_status_url)

    context.push({"repos_status": all_repo_status_response.json()})

    if pid_form.is_valid():
        context.push({"pid_form": pid_form})
        functionality = pid_form.cleaned_data['functionality_field']
        pids = pid_form.cleaned_data['pid_field']
        if functionality != "expanddatatype":
            api_url = API_NETLOC + f'/{functionality}/?pid={",".join(pids)}'
        else:
            api_url = API_NETLOC + f'/{functionality}/?data_type={",".join(pids)}'
        # if functionality == 'fetch':
        #     use_dtr = pid_form.cleaned_data['use_dtr_field']
        #     api_url += "&use_dtr=" + use_dtr

        api_response = requests.get(api_url, verify=settings.VERIFY_SSL)
        if functionality == 'expanddatatype':
            taxonomy_tree = TaxonomyTree(api_response.json())
            context.push({"taxonomy_tree": taxonomy_tree})
        else:
            context.push({f"{functionality}_response": api_response.json()})

        return render(request, f"UI/_{functionality}.html", context.flatten())
    else:
        pid_form: PIDForm = PIDForm(initial={'functionality_field': 'sniff'})
        context.push({"pid_form": pid_form})
        return render(request, "UI/_content.html", context.flatten())
