from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import dog


@api_view()
def get_fetch(request):
    if request.method == 'GET':
        pid_candidate = request.query_params.get('pid', '')
        fetch_result = dog.fetch(pid_candidate)
        return Response(fetch_result)
    else:
        return Response({"Error:" "Requests other than GET not supported"}, status=status)


@api_view(['GET'])
def get_sniff(request):

    pid_candidate = request.query_params.get('pid', '')
    sniff_result = dog.sniff(pid_candidate)
    return Response(sniff_result)
