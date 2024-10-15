"""DOG web application URL Configuration
"""

from django.urls import include, path, re_path
from drf_spectacular.views import SpectacularAPIView, SpectacularJSONAPIView


from dogui.views_ui import about, contact, dtr, home
from dogapi.views_api import (fetch, identify, sniff, is_pid, expand_datatype, get_all_repositories,
                              get_repositories_status)


urlpatterns = [
    re_path(r'api/openapi.yml', SpectacularAPIView.as_view(), name='openapi_schema_yml'),
    re_path(r'api/openapi.json', SpectacularJSONAPIView.as_view(), name='openapi_schema_json'),
    # API
    path('api/fetch/', fetch, name='fetch'),
    path('api/identify/', identify, name='identify'),
    path('api/sniff/', sniff, name='sniff'),
    path('api/ispid/', is_pid, name='is pid'),

    path('__debug__/', include('debug_toolbar.urls')),
    path('api/expanddatatype/', expand_datatype, name='expand data type'),
    path('api/allregrepo/', get_all_repositories, name='get all repositories'),
    path('api/repostatus/', get_repositories_status, name='get repositories status'),

    # UI
    path('', home, name='main'),
    path('about', about, name='about'),
    path('contact', contact, name='contact'),
    path('dtr', dtr, name='contact')
]
