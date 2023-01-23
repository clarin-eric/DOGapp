from drf_yasg import openapi

pid_queryparam: openapi.Parameter = openapi.Parameter(
    name='pid',
    in_=openapi.IN_QUERY,
    description='Persistent identifier/s to a collection',
    type=openapi.TYPE_ARRAY,
    items=openapi.Items(type=openapi.TYPE_STRING))

fetch_response_schema: openapi.Schema = openapi.Schema(
    title="Fetch response schema",
    description="Dictionary of PID's and their respective fetch() call result",
    type=openapi.TYPE_OBJECT,
    required=["pid"],
    properties={
        "pid": openapi.Schema(type=openapi.TYPE_OBJECT,
                              required=["ref_files", "description", "license"],
                              description="Persistent Identifier in form of URL, DOI or HDL",
                              properties={
                                  "ref_files": openapi.Schema(
                                      type=openapi.TYPE_ARRAY,
                                      description="List of referenced resources grouped by type",
                                      items=openapi.Schema(
                                          type=openapi.TYPE_OBJECT,
                                          description="Referenced PID",
                                          required=["resource_type", "pid"],
                                          properties={
                                              "resource_type": openapi.Schema(
                                                  type=openapi.TYPE_STRING,
                                                  description="Type of the referenced resource",
                                                  example="LandingPage"
                                                  ),
                                              "pid": openapi.Schema(
                                                  type=openapi.TYPE_ARRAY,
                                                  description="List of persistent identifier to the \
                                                              referenced resources",
                                                  items=openapi.Schema(
                                                      type=openapi.TYPE_STRING,
                                                      description="Persistent identifier to the \
                                                                  referenced resource of a given type",
                                                      example="http://hdl.handle.net/11022/1009-0000-0000-DD18-D"
                                                  )
                                              )
                                          }
                                      )
                                  ),
                                  "description": openapi.Schema(
                                      type=openapi.TYPE_STRING,
                                      description="Collection's description",
                                      example="wizard-of-oz session"
                                  ),
                                  "license": openapi.Schema(
                                      type=openapi.TYPE_STRING,
                                      description="Collection's license",
                                      example="GPLv3"
                                  )
                              })
    }
)


identify_response_schema: openapi.Schema = openapi.Schema(
    title='Identify response schema',
    description='Identify collection with its title and description',
    type=openapi.TYPE_OBJECT,
    required=["pid"],
    properties={
        "pid": openapi.Schema(type=openapi.TYPE_OBJECT,
                              required=["title", "description"],
                              properties={
                                  "title": openapi.Schema(type=openapi.TYPE_STRING,
                                                          description="Collection's title"),
                                  "description": openapi.Schema(type=openapi.TYPE_STRING,
                                                                description="Collection's description")
                              })
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
    required=["pid"],
    properties={
        "pid": openapi.Schema(type=openapi.TYPE_OBJECT,
                              required=["name", "host_name", "host_netloc"],
                              properties={
                                  "name": openapi.Schema(type=openapi.TYPE_STRING,
                                                         description="Name of the repository"),
                                  "host_name": openapi.Schema(type=openapi.TYPE_STRING,
                                                              description="Name of the hosting service used by a repository"),
                                  "host_netloc": openapi.Schema(type=openapi.TYPE_STRING,
                                                                description="Base URL to the repository")
                              })
    }
)

is_pid_response_schema = openapi.Schema = openapi.Schema(
    title="Is pid response schema",
    description="Is string DOG acceptable PID",
    type=openapi.TYPE_OBJECT,
    required=["pid"],
    properties={
        "pid": openapi.Schema(type=openapi.TYPE_BOOLEAN,
                              description="Is pid acceptable by DOG")
    }
)
