"""DOG web application URL Configuration
"""

from django.urls import include, path, re_path
from drf_spectacular.views import SpectacularAPIView
from rest_framework.permissions import AllowAny

from dogapi.views_api import fetch, identify, is_pid, sniff
from dogui.views_ui import home


urlpatterns = [
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/fetch/', fetch, name='fetch'),
    path('api/identify/', identify, name='identify'),
    path('api/sniff/', sniff, name='sniff'),
    path('api/ispid/', is_pid, name='is pid'),
    path('', home, name='main'),
    path('__debug__/', include('debug_toolbar.urls')),
]
