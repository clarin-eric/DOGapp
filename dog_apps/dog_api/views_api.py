from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.exceptions import MethodNotAllowed, ParseError
from rest_framework.response import Response

from .models import dog


@api_view(['GET'])
def get_fetch(request):
    pid_candidate = request.query_params.get('pid')
    if pid_candidate is None:
        return Response("Missing query parameter 'pid'", status=400)
    fetch_result = dog.fetch(pid_candidate)
    if fetch_result:
        return Response(fetch_result, content_type='application/json', status=200)
    else:
        return Response("PID is either not correct or has been not recognised", status=400)


@api_view(['GET'])
def get_sniff(request):
    pid_candidate = request.query_params.get('pid')
    if pid_candidate is None:
        return Response("Missing query parameter 'pid'", status=400)
    sniff_result = dog.sniff(pid_candidate)
    if sniff_result:
        return Response(sniff_result, content_type='application/json', status=200)
    else:
        return Response("PID is either not correct or has been not recognised", status=400)
