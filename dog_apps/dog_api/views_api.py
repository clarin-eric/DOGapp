from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.exceptions import MethodNotAllowed, ParseError
from rest_framework.response import Response

from .models import dog


@api_view(['GET'])
def get_fetch(request):
    pid_candidate = request.query_params.get('pid')
    if pid_candidate is None:
        raise ParseError(detail="Missing query parameter 'pid'", code=400)
    fetch_result = dog.fetch(pid_candidate)
    return Response(fetch_result)


@api_view(['GET'])
def get_sniff(request):
    pid_candidate = request.query_params.get('pid')
    if pid_candidate is None:
        raise ParseError(detail="Missing query parameter 'pid'", code=400)
    sniff_result = dog.sniff(pid_candidate)
    return Response(sniff_result)
