"""DOG web application URL Configuration
"""

from django.urls import include, path, re_path
from drf_spectacular.views import SpectacularAPIView, SpectacularJSONAPIView
from rest_framework.permissions import AllowAny

<<<<<<< HEAD
from dogapi.views_api import fetch, identify, is_pid, sniff
from dogui.views_ui import home
=======
from dogapi.views_api import fetch, identify, sniff, expand_datatype
>>>>>>> main


urlpatterns = [
<<<<<<< HEAD
    re_path(r'api/openapi.yml', SpectacularAPIView.as_view(), name='openapi_schema_yml'),
    re_path(r'api/openapi.json', SpectacularJSONAPIView.as_view(), name='openapi_schema_json'),

    path('api/fetch/', fetch, name='fetch'),
    path('api/identify/', identify, name='identify'),
    path('api/sniff/', sniff, name='sniff'),
    path('api/ispid/', is_pid, name='is pid'),
    path('', home, name='main'),
    path('__debug__/', include('debug_toolbar.urls')),
=======
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('fetch/', fetch, name='fetch'),
    path('identify/', identify, name='identify'),
    path('sniff/', sniff, name='sniff'),
    path('expanddatatype/', expand_datatype, name='expand data type'),
>>>>>>> main
]
