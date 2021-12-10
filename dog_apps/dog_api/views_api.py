from rest_framework import status
from rest_framework.decorators import api_view, renderer_classes, schema
from rest_framework.exceptions import MethodNotAllowed, ParseError
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.schemas.openapi import AutoSchema
from typing import List, Union
import yaml

from .models import dog


class AutoDocstringSchema(AutoSchema):
    """
    Auto OpenAPI schema generator parsing Python docstrings

    Source:
    https://igeorgiev.eu/python/misc/python-django-rest-framework-openapi-documentation/
    """
    @property
    def documentation(self):
        if not hasattr(self, '_documentation'):
            try:
                self._documentation = yaml.safe_load(self.view.__doc__)
            except yaml.scanner.ScannerError:
                self._documentation = {}
        return self._documentation

    def get_components(self, path, method):
        components = super().get_components(path, method)
        doc_components = self.documentation.get('components', {})
        components.update(doc_components)
        return components

    def get_operation(self, path, method):
        operation = super().get_operation( path, method)
        doc_operation = self.documentation.get(method.lower(), {})
        operation.update(doc_operation)
        return operation


@api_view(['GET'])
@schema(AutoDocstringSchema())
def get_fetch(request):
    """
    get:
        description: Fetches referenced resources from collection's PID
        summary: Fetch referenced resources
        parameters:
          - name: pid
            description: PID referencing a collection
            schema:
                type: string
        responses:
            200:
                description: Resources fetched successfully
                content: 'application/json': {"ref_files": string, "description": string, "license": string}
    """
    pid_candidate = request.query_params.get('pid')
    if pid_candidate is None:
        return Response("Missing query parameter 'pid'", status=400)
    fetch_result = dog.fetch(pid_candidate)
    # empty dict evals to 'not None' reference, cast to bool explicitly
    if fetch_result:
        return Response(fetch_result, status=200)
    else:
        return Response("PID is either not correct or has been not recognised", status=400)


@api_view(['GET'])
@schema(AutoDocstringSchema())
def get_sniff(request):
    """
    get:
        description: Check whether collection's host is a registered repository
        summary: Is registered repository
        parameters:
          - name: pid
            description: PID referencing a collection
            schema:
                type: string
        responses:
            200:
                description: Resources fetched successfully
                content: 'application/json': {"name": string, "host_name": string, "host_netloc": string}
    """
    pid_candidate = request.query_params.get('pid')
    if pid_candidate is None:
        return Response("Missing query parameter 'pid'", status=400)
    sniff_result = dog.sniff(pid_candidate)
    if sniff_result:
        return Response(sniff_result, status=200)
    else:
        return Response("PID is either not correct or has been not recognised", status=400)


@api_view(['GET'])
@schema(AutoDocstringSchema())
def get_identify_collection(request):
    """
    get:
        description: Identify title of the collection and PID to itself.
        summary: Is registered repository
        parameters:
          - name: pid
            description: PID referencing a collection
            schema:
                type: string
        responses:
            200:
                description: Resources fetched successfully
                content: 'application/json': {"collection_title": string, "reverse_pid": string}
    """
    pid_candidate = request.query_params.get('pid')
    if pid_candidate is None:
        return Response("Missing query parameter 'pid'", status=400)
    identify_result = dog.identify(pid_candidate)
    if identify_result:
        return Response(identify_result, status=200)
    else:
        return Response("PID is either not correct or has been not recognised", status=400)


@api_view(['POST'])
@schema(AutoDocstringSchema())
def post_sniff_bulk(request):
    pid_candidates = request.data.get('pids')
    if hasattr(pid_candidates, '__iter__'):
        return Response([dog.sniff(pid_candidate) for pid_candidate in pid_candidates], status=200)
    else:
        return Response("Missing data 'pids', it should contain a list of PIDs to identify", status=400)


@api_view(['POST'])
@schema(AutoDocstringSchema())
def post_fetch_bulk(request):
    pid_candidates = request.data.get('pids')
    if hasattr(pid_candidates, '__iter__'):
        return Response([dog.fetch(pid_candidate) for pid_candidate in pid_candidates], status=200)
    else:
        return Response("Missing data 'pids', it should contain a list of PIDs", status=400)


@api_view(['POST'])
@schema(AutoDocstringSchema())
def post_identify_bulk(request):
    pid_candidates = request.data.get('pids')
    if hasattr(pid_candidates, '__iter__'):
        return Response([dog.identify_(pid_candidate) for pid_candidate in pid_candidates], status=200)
    else:
        return Response("Missing data 'pids', it should contain a list of PIDs", status=400)
