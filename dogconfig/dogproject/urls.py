"""DOG web application URL Configuration
"""

from django.urls import include, path, re_path
from drf_spectacular.views import SpectacularAPIView, SpectacularJSONAPIView
from rest_framework.permissions import AllowAny

from dogapi.views_api import fetch, identify, is_pid, sniff
from dogui.views_ui import home


urlpatterns = [
    re_path(r'api/openapi.yml', SpectacularAPIView.as_view(), name='openapi_schema_yml'),
    re_path(r'api/openapi.json', SpectacularJSONAPIView.as_view(), name='openapi_schema_json'),

    path('api/fetch/', fetch, name='fetch'),
    path('api/identify/', identify, name='identify'),
    path('api/sniff/', sniff, name='sniff'),
    path('api/ispid/', is_pid, name='is pid'),
    path('', home, name='main'),
    path('__debug__/', include('debug_toolbar.urls')),
]
