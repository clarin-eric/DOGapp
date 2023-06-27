from django.conf import settings
from drf_spectacular.utils import extend_schema, OpenApiExample, OpenApiParameter
from drf_spectacular.types import OpenApiTypes
import logging.config
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.request import Request
from typing import List

from .models import dog
from .schemas import pid_queryparam
from .serializers import FetchResultSerializer, IdentifyResponseSerializer
from .utils import parse_queryparam, QueryparamParsingError


logging.config.dictConfig(settings.LOGGING)
logger = logging.getLogger(__name__)


@extend_schema(parameters=[pid_queryparam],
               description="Fetches all PIDs referenced in the metadata by resource type. For response object \
                           specification please consult examples.",
               responses={
                   200: OpenApiTypes.OBJECT,
                   400: OpenApiTypes.STR
               },
               request=None,
               examples=[
                   OpenApiExample(
                       name="Successful fetch result example",
                       description="Fetch referenced resources from the metadata. "
                                   "Due to drf-spectacular not supporting variable keys documentation generation, the output type "
                                   "specification is available only through the description and examples for the time being",
                       value=[
                           {"https://lindat.mff.cuni.cz/repository/xmlui/handle/11234/1-3422": {
                               "ref_files": [
                                   {
                                       "resource_type": "Resource",
                                       "pid": [
                                           "http://radio.makon.cz/",
                                           "https://lindat.mff.cuni.cz/repository/xmlui/bitstream/handle/11234/1-3422/README?sequence=1]}",
                                           "...",
                                           "https://lindat.mff.cuni.cz/repository/xmlui/bitstream/handle/11234/1-3422/makon-plzen2.zip?sequence=33"
                                       ]
                                   },
                                   {
                                       "resource_type": "LandingPage",
                                       "pid": ["https://hdl.handle.net/11234/1-3422"]}
                               ],
                               "description": "Talks of Karel Makoň given to his friends in the course of late sixties through early nineties of the 20th century. The topic is mostly christian mysticism.",
                               "license": "http://creativecommons.org/licenses/by-sa/4.0/",
                               "failure": 0,
                           }}],
                       response_only=True
                   ),
                   OpenApiExample(
                       name="Failed fetch result example",
                       description="There are no referenced resources in the metadata. "
                                   "Due to drf-spectacular not supporting variable keys documentation generation, the output type "
                                   "specification is available only through the description and examples for the time being",
                       value={"<definitelyNotAPID>": {
                               "failure": 1,
                               "failure_message": "Persistent Identifier could not be resolved or metadata could not be parsed"
                           }},
                       response_only=True
                   )
               ])
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
        fetch_result: dict = {pid: dog.fetch(pid) for pid in pids}
        if not bool(fetch_result):
            ret = Response(f"All Persistent Identifiers are either incorrect or unrecognised", status=400)
        else:
            fetch_result = {pid: ({**result, **{"failure": 0}} if result else
                                  {"failure": 2,
                                   "failure_message": "Persistent Identifier could not be resolved or parsed"})
                            for pid, result in fetch_result.items()}
            fetch_result = {pid: FetchResultSerializer(ref_files).data
                            for pid, ref_files in fetch_result.items()
                            if ref_files["failure"] == 0}
            ret = Response(fetch_result, status=200)
    except QueryparamParsingError as err:
        ret = Response(err, status=400)

    return ret


@extend_schema(parameters=[pid_queryparam],
               description="Identifies collection with its title and description, functionality requested for "
                           "Virtual Content Registry. For response object specification please consult examples.",
               responses={
                   200: OpenApiTypes.OBJECT,
                   400: OpenApiTypes.STR
               },
               request=None,
               examples=[
                   OpenApiExample(
                       name="Successfully identified result example",
                       description="Collection has been identified. "
                                   "Due to drf-spectacular not supporting variable keys documentation generation, the output type "
                                   "specification is available only through the description and examples for the time being",
                       value={"https://lindat.mff.cuni.cz/repository/xmlui/handle/11234/1-3422":
                                  {'item_title': 'LINDAT / CLARIAH-CZ Data & Tools',
                                   'description': 'Talks of Karel Makoň given to his friends in the course of late sixties through early nineties of the 20th century. The topic is mostly christian mysticism.',
                                   'reverse_pid': 'https://hdl.handle.net/11234/1-3422@format=cmdi'}
                              },
                       response_only=True
                   ),
                   OpenApiExample(
                       name="Failed result identification example",
                       description="There are no referenced resources in the metadata "
                                   "Due to drf-spectacular not supporting variable keys documentation generation, the output type "
                                   "specification is available only through the description and examples for the time being",
                       value={"<definitelyNotAPID>": {}},
                       response_only=True
                   )
               ])
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
            ret = Response(f"All Persistent Identifiers are either incorrect or unrecognised", status=400)
    except QueryparamParsingError as err:
        ret = Response(err, status=400)

    return ret


@extend_schema(parameters=[pid_queryparam],
               description="Checks if PIDs points to a metadata referencing another resource(s). For response object \
                           specification please consult examples.",
               responses={
                   200: OpenApiTypes.OBJECT,
                   400: OpenApiTypes.STR
               },
               request=None,
               examples=[
                   OpenApiExample(
                       name="Input PID points to a collection",
                       description="Checks if PID points to a metadata referenging another resource(s)"
                                   "Due to drf-spectacular not supporting variable keys documentation generation, the output type"
                                   "specification is available only through the description and examples for the time being",
                       value={"https://lindat.mff.cuni.cz/repository/xmlui/handle/11234/1-3422": True},
                       response_only=True
                   ),
                   OpenApiExample(
                       name="Input PID does not point to a collection",
                       description="Checks if PID points to a metadata referenging another resource(s)"
                                   "Due to drf-spectacular not supporting variable keys documentation generation, the output type "
                                   "specification is available only through the description and examples for the time being",
                       value={"https://lindat.mff.cuni.cz/repository/xmlui/bitstream/handle/11234/1-3422/makon-plzen1.zip?sequence=32": False},
                       response_only=True
                   )
               ])
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
            ret = Response(f"All Persistent Identifiers are either incorrect or unrecognised", status=400)
    except QueryparamParsingError as err:
        ret = Response(err, status=400)
    return ret


@extend_schema(parameters=[pid_queryparam],
               description="Checks whether input PIDs points to a resource hosted by Registered Repository",
               responses={
                   200: OpenApiTypes.OBJECT,
                   400: OpenApiTypes.STR
               },
               request=None,
               examples=[
                   OpenApiExample(
                       name="Successful sniff result example",
                       description="Host repository details ",
                       value=[
                           {
                               "https://lindat.mff.cuni.cz/repository/xmlui/handle/11234/1-3422": {
                                   "name": "LINDAT/CLARIAH-CZ",
                                   "host_name": "LINDAT/CLARIAH-CZ",
                                   "host_netloc": "https://lindat.mff.cuni.cz",
                                   "failure": 0
                               }
                           }
                       ],
                       response_only=True
                   ),
                   OpenApiExample(
                       name="Failed sniff result example",
                       description="Host sniff details",
                       value=[
                           {
                               "<definitelyNotAPID>": {},
                               "failure": 1,
                               "failure_message": "Persistent Identifier could not be resolved or metadata could not be parsed"
                           }
                       ],
                       response_only=True
                   )
               ]
               )
@permission_classes([AllowAny])
@api_view(['GET'])
def sniff(request: Request) -> Response:
    """
    Checks whether PID points to a resources in a Registered Repository:
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
        sniff_result = {pid: ({**result, **{"failure": 0}} if result else
                              {"failure": 2, "failure_message": "Persistent Identifier could not be resolved or parsed"})
                        for pid, result in sniff_result.items()}

        if sniff_result:
            ret = Response(sniff_result, status=200)
        else:
            ret = Response(f"All Persistent Identifiers are either incorrect or unrecognised", status=400)
    except QueryparamParsingError as err:
        ret = Response(err, status=400)
    return ret

@extend_schema(parameters=[pid_queryparam],
               description="Checks whether input is a PID that can be parsed by DOG. Does only string parsing. "
                           "Any valid string in a format of URL, DOI or HDL will be accepted. "
                           "A valid PID string does not imply valid string ",
               responses={
                   200: OpenApiTypes.OBJECT,
                   400: OpenApiTypes.STR
               },
               request=None,
               examples=[
                   OpenApiExample(
                       name="Successful sniff result example",
                       description="Host repository details ",
                       value=[
                           {
                               "https://lindat.mff.cuni.cz/repository/xmlui/handle/11234/1-3422": {
                                   "name": "LINDAT/CLARIAH-CZ",
                                   "host_name": "LINDAT/CLARIAH-CZ",
                                   "host_netloc": "https://lindat.mff.cuni.cz",
                                   "failure": 0
                               }
                           }
                       ],
                       response_only=True
                   ),
                   OpenApiExample(
                       name="Failed sniff result example",
                       description="Host sniff details",
                       value=[
                           {
                               "<definitelyNotAPID>": {},
                               "failure": 1,
                               "failure_message": "Persistent Identifier could not be resolved or metadata could not be parsed"
                           }
                       ],
                       response_only=True
                   )
               ]
               )
@permission_classes([AllowAny])
@api_view(['GET'])
def is_pid(request: Request) -> Response:
    ret: Response
    try:
        pids = parse_queryparam(request, "pid")
        pid_result = {pid: True if dog.is_pid(pid) is not None else False for pid in pids}
        ret = Response(pid_result, status=200)
    except QueryparamParsingError as err:
        ret = Response(err, status=400)
    return ret
