"""
Note, that @api_view decorator must follow @swagger_auto_schema to enable different schemas to be served for different
methods
"""
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.request import Request
from typing import List

from .models import dog, doglib_expand_datatype
from .schemas import fetch_response_schema, identify_response_schema, is_collection_response_schema, pid_queryparam, \
    sniff_response_schema


def parse_queryparam(request: Request, param_name: str) -> List[str]:
    """
    Parses queryparameters from direct API call (PHP-like format ?param[]=val1&param[]=val2, both with and without [])
    and via Swagger UI (?param=val1,val2)
    """
    query_param_candidates = request.GET.getlist(param_name)
    # Swagger UI returns a 1 element list with comma separated values of parameter, e.g. ["string,string,string"]
    param_candidates = [param for param_candidate in query_param_candidates for param in param_candidate.split(',')]
    return param_candidates


@swagger_auto_schema(method="get",
                     manual_parameters=[pid_queryparam],
                     operation_description="Fetches all PIDs referenced in the metadata",
                     responses={200: fetch_response_schema,
                                400: "Persistent Identifier(s) {pids} is either not correct or has been not recognised"}
                     )
@permission_classes([AllowAny])
@api_view(['GET'])
def fetch(request: Request) -> Response:
    """
    Fetches all PIDs referenced in the metadata, supports PID and list of PIDs to metadata in formats:
    ?pid=val1&pid=val2&pid=val3
    ?pid=val1,val2,val3

    Returns [{pid: {fetch_results}}]
    """
    pids = parse_queryparam(request, 'pid')
    fetch_results = {pid: dog.fetch(pid) for pid in pids}
    if fetch_results:
        return Response(fetch_results, status=200)
    else:
        return Response(f"Persistent Identifier(s) {pids} is either not correct or has been not recognised", status=400)


@swagger_auto_schema(method="get",
                     manual_parameters=[pid_queryparam],
                     operation_description="Identifies PID",
                     responses={200: identify_response_schema,
                                400: "Persistent Identifier(s) {pids} is either not correct or has been not recognised"}
                     )
@permission_classes([AllowAny])
@api_view(['GET'])
def identify(request: Request) -> Response:
    """
    Identifies PID (VLO request):
    ?pid=val1&pid=val2&pid=val3
    ?pid=val1,val2,val3

    Returns [{pid: <identify_result>}]
    """
    pids = parse_queryparam(request, 'pid')
    identify_result = {pid: dog.identify(pid) for pid in pids}
    if identify_result:
        return Response(identify_result, status=200)
    else:
        return Response(f"Persistent Identifier(s) {pids} is either not correct or has been not recognised", status=400)


@swagger_auto_schema(method="get",
                     manual_parameters=[pid_queryparam],
                     operation_description="Checks whether PID points to a collection",
                     responses={200: is_collection_response_schema,
                                400: "Persistent Identifier(s) {pids} is either not correct or has been not recognised"}
                     )
@permission_classes([AllowAny])
@api_view(['GET'])
def is_collection(request: Request) -> Response:
    """
    Checks whether PID points to a collection:
    ?pid=<val1>&pid=<val2>&pid=<val3>
    ?pid=<val1>,<val2>,<val3>

    Returns [{pid: bool}]
    """
    pids = parse_queryparam(request, 'pid')
    is_collection_result = {pid: dog.is_collection(pid) for pid in pids}
    if is_collection_result:
        return Response(is_collection_result, status=200)
    else:
        return Response(f"Persistent Identifier(s) {pids} is either not correct or has been not recognised", status=400)


@swagger_auto_schema(method="get",
                     manual_parameters=[pid_queryparam],
                     operation_description="Checks whether PID points to resources in registered repository",
                     responses={200: sniff_response_schema,
                                400: "Persistent Identifier(s) {pids} is either not correct or has been not recognised"}
                     )
@permission_classes([AllowAny])
@api_view(['GET'])
def sniff(request: Request) -> Response:
    """
    Checks whether PID points to resources in registered repository:
    ?pid=<val1>&pid=<val2>&pid=<val3>
    ?pid=<val1>,<val2>,<val3>

    Returns [{pid: <sniff_result>}]
    """
    pids = parse_queryparam(request, 'pid')
    sniff_result = {pid: dog.sniff(pid) for pid in pids}
    if sniff_result:
        return Response(sniff_result, status=200)
    else:
        return Response(f"Persistent Identifier(s) {pids} is either not correct or has been not recognised", status=400)


@permission_classes([AllowAny])
@api_view(['GET'])
def expand_datatype(request: Request) -> Response:
    data_types = parse_queryparam(request, 'data_type')
    expanded_datatypes: dict = {}
    for data_type in data_types:
        expanded_datatypes.update(doglib_expand_datatype(data_type))
    if expanded_datatypes:
        return Response(expanded_datatypes, status=200)
    else:
        return Response(f"MIME data type(s) {data_types} is either not correct or has been not recognised", status=400)
