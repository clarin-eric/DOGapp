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


def home(request: HttpRequest) -> HttpResponse:
    context: RequestContext = RequestContext(request)
    pid_form: PIDForm() = PIDForm(request.GET)

    all_repo_status_url = API_NETLOC + "/repostatus/"
    all_repo_status_response = requests.get(all_repo_status_url,
                                            verify=settings.VERIFY_SSL)

    context.push({"repos_status": all_repo_status_response.json()})
    context.push({"DTR_ENABLED": DTR_ENABLED})

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

        #TODO move DTR to separate application
        # if functionality == 'expanddatatype':
        #     taxonomy_tree = TaxonomyTree(api_response.json())
        #     context.push({"taxonomy_tree": taxonomy_tree})
        # else:
        #     context.push({f"{functionality}_response": api_response.json()})

        context.push({f"{functionality}_response": api_response.json()})

        context.push({"view": functionality})
        return render(request, f"UI/_{functionality}.html", context.flatten())
    else:
        pid_form: PIDForm = PIDForm(initial={'functionality_field': 'sniff'})
        context.push({"pid_form": pid_form})
        context.push({"view": "home"})
        return render(request, "UI/_content.html", context.flatten())


def about(request: HttpRequest) -> HttpResponse:
    context: RequestContext = RequestContext(request)
    context.push({"view": "about"})
    context.push({"DTR_ENABLED": DTR_ENABLED})
    return render(request, "UI/_about.html", context.flatten())


def contact(request: HttpRequest) -> HttpResponse:
    context: RequestContext = RequestContext(request)
    context.push({"view": "contact"})
    context.push({"DTR_ENABLED": DTR_ENABLED})
    return render(request, "UI/_contact.html", context.flatten())


def dtr(request: HttpRequest) -> HttpResponse:
    context: RequestContext = RequestContext(request)
    context.push({"view": "dtr"})
    context.push({"DTR_ENABLED": DTR_ENABLED})
    return render(request, "UI/_dtr.html", context.flatten())
