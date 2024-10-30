from drf_spectacular.utils import OpenApiParameter, OpenApiExample


mimetype_parameter: OpenApiParameter = OpenApiParameter(name='MIMEtype',
                                                        location=OpenApiParameter.QUERY,
                                                        description='MIMEtype(s)',
                                                        required=True,
                                                        type={'type': 'array',
                                                              'items': {'type': 'string'}},
                                                        examples=[
                                                            OpenApiExample(
                                                                'singleton',
                                                                description='Singleton MIMEtype',
                                                                value='text/xml'),
                                                            OpenApiExample(
                                                                'array',
                                                                description='Array of MIMEtypes',
                                                                value='[text/xml, application/x-cmdi+xml]'
                                                            ),
                                                        ])
