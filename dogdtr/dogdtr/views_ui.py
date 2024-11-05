from django.conf import settings
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.template import RequestContext
import logging.config


from .utils import TaxonomyTree
from .forms import MIMETypeForm

logging.config.dictConfig(settings.LOGGING)

API_NETLOC = settings.API_NETLOC
DTR_ENABLED = settings.DTR_ENABLED
VERIFY_SSL = settings.VERIFY_SSL


def dtr(request: HttpRequest) -> HttpResponse:
    context: RequestContext = RequestContext(request)
    mimetype_form: MIMETypeForm = MIMETypeForm(request.GET)

    if pid_form.is_valid():
        context.push({"mimetype_form": mimetype_form})
        pids = mimetype_form.cleaned_data['mimetype_field']
        api_url = API_NETLOC + f'/expanddatatype/?data_type={",".join(pids)}'

        api_response = requests.get(api_url, verify=VERIFY_SSL)


    context: RequestContext = RequestContext(request)
    context.push({"view": "dtr"})
    context.push({"DTR_ENABLED": DTR_ENABLED})
    return render(request, "UI/_dtr.html", context.flatten())
