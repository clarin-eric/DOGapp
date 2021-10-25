from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.exceptions import MethodNotAllowed, ParseError
from rest_framework.response import Response
from typing import List, Union

from .models import dog


@api_view(['GET'])
def get_fetch(request):
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
def get_sniff(request):
    pid_candidate = request.query_params.get('pid')
    if pid_candidate is None:
        return Response("Missing query parameter 'pid'", status=400)
    sniff_result = dog.sniff(pid_candidate)
    if sniff_result:
        return Response(sniff_result, status=200)
    else:
        return Response("PID is either not correct or has been not recognised", status=400)


@api_view(['POST'])
def post_sniff_bulk(request):
    pid_candidates = request.data.get('pids')
    if hasattr(pid_candidates, '__iter__'):
        return Response([dog.sniff(pid_candidate) for pid_candidate in pid_candidates], status=200)
    else:
        return Response("Bulk sniff requires parameter 'pids' with iterable yielding PIDs", status=400)


@api_view(['POST'])
def post_fetch_bulk(request):
    pid_candidates = request.data.get('pids')
    if hasattr(pid_candidates, '__iter__'):
        return Response([dog.fetch(pid_candidate) for pid_candidate in pid_candidates], status=200)
    else:
        return Response("Bulk fetch requires parameter 'pids' with iterable yielding PIDs", status=400)
