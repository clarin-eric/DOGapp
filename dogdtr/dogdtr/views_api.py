from django.conf import settings
from django.core.cache import cache
from dataclasses import asdict
from drf_spectacular.utils import extend_schema, OpenApiExample
from drf_spectacular.types import OpenApiTypes
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.request import Request


from dogapi.utils import parse_queryparam


@extend_schema(parameters=[],
               description="Returns taxonomy of a MIME type according to Data Type Registry",
               responses={
                   200: OpenApiTypes.OBJECT,
                   400: OpenApiTypes.STR
               },
               request=None,
               examples=[
               ]
               )
@permission_classes([AllowAny])
@api_view(['GET'])
def expand_datatype(request: Request) -> Response:
    data_types = parse_queryparam(request, 'data_type')
    expanded_datatypes: dict = {}
    for data_type in data_types:
        expanded_datatypes[data_type] = doglib_expand_datatype(data_type)
    if expanded_datatypes:
        return Response(expanded_datatypes, status=200)
    else:
        return Response(f"MIME data type(s) {data_types} is either not correct or has been not recognised",
                        status=400)