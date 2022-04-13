from drf_yasg import openapi

pid_queryparam: openapi.Parameter = openapi.Parameter(
    name='pid',
    in_=openapi.IN_QUERY,
    description='Persistent identifier to a collection',
    type=openapi.TYPE_ARRAY,
    items=openapi.Items(type=openapi.TYPE_STRING))

fetch_response_schema: openapi.Schema = openapi.Schema(
    title='Fetch response schema',
    description='Schema of the response of doglib.fetch() call',
    type=openapi.TYPE_OBJECT,
    additional_properties=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        additional_properties=True
    )
)

identify_response_schema: openapi.Schema = openapi.Schema(
    title='Identify response schema',
    description='Schema of the response of doglib.identify() call',
    type=openapi.TYPE_OBJECT,
    additional_properties=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        additional_properties=openapi.Schema(
            type=openapi.TYPE_STRING
        )
    )
)

is_collection_response_schema: openapi.Schema = openapi.Schema(
    title='Is collection response schema',
    description='Schema of the response of doglib.is_collection() call',
    type=openapi.TYPE_OBJECT,
    additional_properties=openapi.Schema(
        type=openapi.TYPE_BOOLEAN
    )

)

sniff_response_schema: openapi.Schema = openapi.Schema(
    title='Identify response schema',
    description='Schema of the response of doglib.identify() call',
    type=openapi.TYPE_OBJECT,
    additional_properties=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        additional_properties=True
    )
)