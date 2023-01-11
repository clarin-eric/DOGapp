"""DOG web application URL Configuration
"""

from django.urls import include, path, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework.permissions import AllowAny

from dogapi.views_api import fetch, identify, is_pid, sniff
from dogui.views_ui import home

openapi_info = openapi.Info(title="DOG API",
                            default_version='v2',
                            description="Digital Object Gate API",
                            terms_of_service="",
                            contact=openapi.Contact(email="michal@clarin.eu"),
                            license=openapi.License(name="GPLv3"))
# TODO serve as static file
schema_view = get_schema_view(openapi_info,
                              public=True,
                              permission_classes=[AllowAny]
                              )

urlpatterns = [
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('api/fetch/', fetch, name='fetch'),
    path('api/identify/', identify, name='identify'),
    path('api/sniff/', sniff, name='sniff'),
    path('api/ispid/', is_pid, name='is pid'),
    path('', home, name='main'),
    path('__debug__/', include('debug_toolbar.urls')),
]
