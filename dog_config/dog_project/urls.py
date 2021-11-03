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
from rest_framework.schemas import get_schema_view

from dog_api.views_api import get_fetch, post_fetch_bulk, get_sniff, post_sniff_bulk


urlpatterns = [
    path('sniff/', get_sniff, name='sniff'),
    path('fetch/', get_fetch, name='fetch'),
    path('sniff_bulk/', post_sniff_bulk, name='bulk sniff'),
    path('fetch_bulk/', post_fetch_bulk, name='bulk fetch'),
    path('openapi/', get_schema_view(title="Digital Object Gate", description="REST API providing Digital Object Gate's functionalities"), name='openapi-schema')
]
