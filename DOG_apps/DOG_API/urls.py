# minimal_django/api/urls.py
from django.conf.urls import include, url
from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import get_fetch, get_sniff

router = DefaultRouter()
router.register(r'sniff/<slug:pid>', get_sniff, basename='sniff')
router.register(r'fetch/<slug:pid>', get_fetch, basename='fetch')

urlpatterns = [
    path('', include(router.urls))
]
