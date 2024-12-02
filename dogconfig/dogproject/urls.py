"""DOG web application URL Configuration
"""

from django.urls import include, path, re_path
from drf_spectacular.views import SpectacularAPIView, SpectacularJSONAPIView


from dogapi.views_api import (fetch, identify, sniff, is_pid, get_all_repositories,
                              get_repositories_status)
from dogdtr.views_api import expand_datatype_view

from dogdtr.views_ui import dtr
from dogui.views_ui import about, contact, home



urlpatterns = [
    re_path(r'api/v1/openapi.yml', SpectacularAPIView.as_view(), name='openapi_schema_yml'),
    re_path(r'api/v1/openapi.json', SpectacularJSONAPIView.as_view(), name='openapi_schema_json'),
    # API
    path('api/v1/fetch/', fetch, name='fetch'),
    path('api/v1/identify/', identify, name='identify'),
    path('api/v1/sniff/', sniff, name='sniff'),
    path('api/v1/ispid/', is_pid, name='is pid'),

    path('__debug__/', include('debug_toolbar.urls')),
    path('api/v1/expanddatatype/', expand_datatype_view, name='expand data type'),
    path('api/v1/allregrepo/', get_all_repositories, name='get all repositories'),
    path('api/v1/repostatus/', get_repositories_status, name='get repositories status'),

    # UI
    path('', home, name='main'),
    path('about/', about, name='about'),
    path('contact/', contact, name='contact'),
    path('dtr/', dtr, name='dtr'),
]
