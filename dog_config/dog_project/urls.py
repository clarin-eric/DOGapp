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
from django.conf.urls import include, url
from django.urls import path
from rest_framework.routers import DefaultRouter

from dog_api.views_api import get_fetch, get_sniff

router = DefaultRouter()
router.register(r'sniff/<path:pid>/', get_sniff, basename='sniff')
router.register(r'fetch/<path:pid>/', get_fetch, basename='fetch')

urlpatterns = [
    path('', include(router.urls))
]