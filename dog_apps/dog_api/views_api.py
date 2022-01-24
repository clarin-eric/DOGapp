"""

Note, that @api_view decorator must follow @swagger_auto_schema to enable different schemas to be served for different methods
"""
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.request import Request
from typing import List

from .models import dog


def parse_pid_queryparam(request: Request) -> List[str]:
    """
    Parses queryparameters from direct API call (PHP-like format ?param=val1&param=val2) and via Swagger UI (?param=val1,val2)
    """
    query_pid_candidates = request.GET.getlist('pid')
    pid_candidates = []
    # Swagger UI returns a 1 element list with comma separated values of parameter, e.g. ["string,string,string"]
    for pid_candidate in query_pid_candidates:
        pid_candidates.extend(pid_candidate.split(','))
    return pid_candidates


pid_queryparam: openapi.Parameter = openapi.Parameter(name='pid',
                                                      in_=openapi.IN_QUERY,
                                                      description='Persistent identifier to a collection',
                                                      type=openapi.TYPE_ARRAY,
                                                      items=openapi.Items(type=openapi.TYPE_STRING))


# TODO, explicit declaration of Response format (drf_yasg unable to infer from modelless serializers)
@swagger_auto_schema(method="get", manual_parameters=[pid_queryparam])
@permission_classes([AllowAny])
@api_view(['GET'])
def fetch(request: Request) -> Response:
    """
    Call to doglib.fetch(), supports PID and list of PIDs in formats:
    ?pid=<pid1>&pid=<pid2>&pid=<pid3>
    ?pid=<pid1>,<pid2>,<pid3>

    Returns [{<pid>: {fetch_results}}]
    """
    pids = parse_pid_queryparam(request)
    fetch_results = {pid: dog.fetch(pid) for pid in pids}
    if fetch_results:
        return Response(fetch_results, status=200)
    else:
        return Response(f"Persistent Identifier(s) {pids} is either not correct or has been not recognised", status=400)


# TODO, explicit declaration of Response format (drf_yasg unable to infer from modelless serializers)
@swagger_auto_schema(method="get", manual_parameters=[pid_queryparam])
@permission_classes([AllowAny])
@api_view(['GET'])
def identify(request: Request) -> Response:
    """
    Call to doglib.fetch(), supports PID and list of PIDs in formats:
    ?pid=<pid1>&pid=<pid2>&pid=<pid3>
    ?pid=<pid1>,<pid2>,<pid3>

    Returns [{<pid>: {identify_result}}]
    """
    pids = parse_pid_queryparam(request)
    identify_result = {pid: dog.identify(pid) for pid in pids}
    if identify_result:
        return Response(identify_result, status=200)
    else:
        return Response(f"Persistent Identifier(s) {pids} is either not correct or has been not recognised", status=400)


# TODO, explicit declaration of Response format (drf_yasg unable to infer from modelless serializers)
@swagger_auto_schema(method="get", manual_parameters=[pid_queryparam])
@permission_classes([AllowAny])
@api_view(['GET'])
def sniff(request: Request) -> Response:
    """
    Call to doglib.sniff(), supports list of parameters in format ?pid=<pid1>&pid=<pid2>&pid=<pid3>

    Returns [{<pid>: {sniff_result}}]
    """
    pids = parse_pid_queryparam(request)
    sniff_result = {pid: dog.identify(pid) for pid in pids}
    if sniff_result:
        return Response(sniff_result, status=200)
    else:
        return Response(f"Persistent Identifier(s) {pids} is either not correct or has been not recognised", status=400)
