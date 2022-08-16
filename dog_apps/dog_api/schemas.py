from drf_yasg import openapi


pid_queryparam: openapi.Parameter = openapi.Parameter(
    name='pid',
    in_=openapi.IN_QUERY,
    description='Persistent identifier to a collection',
    type=openapi.TYPE_ARRAY,
    items=openapi.Items(type=openapi.TYPE_STRING))

fetch_response_schema: openapi.Schema = openapi.Schema(
    title="Fetch response schema",
    description="Parse referenced PID's",
    type=openapi.TYPE_OBJECT,
    required=["ref_files", "description", "license"],
    properties={
        "ref_files": openapi.Schema(type=openapi.TYPE_ARRAY,
                                    description="Referenced PIDs in collection metadata",
                                    items=openapi.Schema(type=openapi.TYPE_STRING,
                                                         description="Referenced PID")),
        "description": openapi.Schema(type=openapi.TYPE_STRING,
                                      description="Collection's description"),
        "license": openapi.Schema(type=openapi.TYPE_STRING,
                                  description="Collection's license")
    }
)

identify_response_schema: openapi.Schema = openapi.Schema(
    title='Identify response schema',
    description='Identify collection with its title and description',
    type=openapi.TYPE_OBJECT,
    required=["title", "description"],
    properties={
        "title": openapi.Schema(type=openapi.TYPE_STRING,
                                description="Collection's title"),
        "description": openapi.Schema(type=openapi.TYPE_STRING,
                                      description="Collection's description")
    }
)

is_collection_response_schema: openapi.Schema = openapi.Schema(
    title='Is collection response schema',
    description='Check whether PID points to another collection',
    type=openapi.TYPE_BOOLEAN
)

sniff_response_schema: openapi.Schema = openapi.Schema(
    title="Sniff response schema",
    description="Collection's host repository identification",
    type=openapi.TYPE_OBJECT,
    required=["name", "host_name", "host_netloc"],
    properties={
        "name": openapi.Schema(type=openapi.TYPE_STRING,
                               description="Name of the repository"),
        "host_name": openapi.Schema(type=openapi.TYPE_STRING,
                                    description="Name of the hosting service used by a repository"),
        "host_netloc": openapi.Schema(type=openapi.TYPE_STRING,
                                      description="Base URL to the repository")
    }
)