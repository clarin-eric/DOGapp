from drf_spectacular.utils import extend_schema, OpenApiExample
from drf_spectacular.types import OpenApiTypes
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.request import Request


from dogapi.utils import parse_queryparam


from .dtr import expand_datatype
from .schemas import mimetype_parameter
from .utils import parse_queryparam


@extend_schema(parameters=[mimetype_parameter],
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
def expand_datatype_view(request: Request) -> Response:
    mime_types = parse_queryparam(request, 'mimetype')
    expanded_datatypes: dict = {}
    for data_type in mime_types:
        expanded_datatypes[data_type] = expand_datatype(data_type)
    if expanded_datatypes:
        return Response(expanded_datatypes, status=200)
    else:
        return Response(f"MIME data type(s) {mime_types} is either not correct or has been not recognised",
                        status=400)
