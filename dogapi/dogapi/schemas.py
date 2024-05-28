from drf_spectacular.utils import OpenApiParameter, OpenApiExample



pid_queryparam: OpenApiParameter = OpenApiParameter(name='pid',
                                                    location=OpenApiParameter.QUERY,
                                                    description='Persistent identifier(s)',
                                                    required=True,
                                                    type={'type': 'array',
                                                          'items': 'str'},
                                                    examples=[
                                                        OpenApiExample(
                                                            'HDL',
                                                            description='Handle',
                                                            value='http://hdl.handle.net/21.11115/0000-000C-4E21-8'),
                                                        OpenApiExample(
                                                            'DOI',
                                                            description='Digital Object Identifier',
                                                            value='https://doi.org/10.15155/9-00-0000-0000-0000-001ABL'
                                                        ),
                                                        OpenApiExample(
                                                            'URL',
                                                            description='Uniform Resource Locator',
                                                            value='https://clarin-pl.eu/dspace/handle/11321/6?format=cmdi'
                                                        )
                                                    ])
use_dtr_queryparam: OpenApiParameter = OpenApiParameter(name='use_dtr',
                                                        location=OpenApiParameter.QUERY,
                                                        description='flag whether expand MIMETypes with DTR',
                                                        required=False,
                                                        type={'type': "boolean"},
                                                        examples=[
                                                            OpenApiExample(
                                                                'True',
                                                                description='Do use DTR',
                                                                value='True'
                                                            ),
                                                            OpenApiExample(
                                                                'False',
                                                                description='Do NOT use DTR',
                                                                value='False')
                                                        ])
