"""DOG-apps URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework.permissions import AllowAny

from dogapi.views_api import fetch, identify, sniff
from dogui.views import form_pid, sniff_result

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
]
