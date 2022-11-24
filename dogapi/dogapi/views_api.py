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


from .models import dog
from .schemas import fetch_response_schema, identify_response_schema, is_collection_response_schema, pid_queryparam, \
    sniff_response_schema
from .utils import parse_queryparam, QueryparamParsingError


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

    :param request: Django REST Framework request instance
    :type request: rest_framework.response.Request

    :return: Django REST Framework response instance containing list of dicts in format [{pid: <fetch_result>}]
    :rtype: rest_framework.response.Response
    """
    ret: Response
    try:
        pids = parse_queryparam(request, "pid")
        fetch_results = {pid: dog.fetch(pid) for pid in pids}
        if fetch_results:
            ret = Response(fetch_results, status=200)
        else:
            ret = Response(f"Persistent Identifier(s) {pids} is either not correct or has been not recognised", status=400)
    except QueryparamParsingError as err:
        ret = Response(err, status=400)

    return ret


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
    Identifies PID:
    ?pid=val1&pid=val2&pid=val3
    ?pid=val1,val2,val3

    :param request: Django REST Framework request instance
    :type request: rest_framework.response.Request

    :return: Django REST Framework response instance containing list of dicts in format [{pid: <identify_result>}]
    :rtype: rest_framework.response.Response
    """
    ret: Response
    try:
        pids: List[str] = parse_queryparam(request, "pid")
        identify_result = {pid: dog.identify(pid) for pid in pids}
        if identify_result:
            ret = Response(identify_result, status=200)
        else:
            ret = Response(f"Persistent Identifier(s) {pids} is either not correct or has been not recognised",
                           status=400)
    except QueryparamParsingError as err:
        ret = Response(err, status=400)

    return ret


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

    :param request: Django REST Framework request instance
    :type request: rest_framework.response.Request

    :return: Django REST Framework response instance containing list of dicts in format [{pid: <is_collection_result>]
    :rtype: rest_framework.response.Response
    """
    ret: Response
    try:
        pids: List[str] = parse_queryparam(request, "pid")
        is_collection_result: dict = {pid: dog.is_collection(pid) for pid in pids}
        if is_collection_result:
            ret = Response(is_collection_result, status=200)
        else:
            ret = Response(f"Persistent Identifier(s) {pids} is either not correct or has been not recognised", status=400)
    except QueryparamParsingError as err:
        ret = Response(err, status=400)

    return ret


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

    :param request: Django REST Framework request instance
    :type request: rest_framework.response.Request

    :return: Django REST Framework response instance containing list of dicts in format [{pid: <sniff_result>]
    :rtype: rest_framework.response.Response
    """
    ret: Response
    try:
        pids = parse_queryparam(request, "pid")
        sniff_result = {pid: dog.sniff(pid) for pid in pids}
        if sniff_result:
            ret = Response(sniff_result, status=200)
        else:
            ret = Response(f"Persistent Identifier(s) {pids} is either not correct or has been not recognised", status=400)
    except QueryparamParsingError as err:
        ret = Response(err, status=400)

    return ret
