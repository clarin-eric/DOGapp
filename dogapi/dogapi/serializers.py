"""Serializer classes for drf_spectacular OpenAPI 3.0 documentation"""

from drf_spectacular.utils import extend_schema, extend_schema_field, OpenApiParameter, OpenApiExample
from drf_spectacular.types import OpenApiTypes
from rest_framework.request import Request
from typing import TypedDict, List, Union

from rest_framework import serializers


class _RefResourcesSerializer(serializers.Serializer):
    resource_type = serializers.CharField()
    pid = serializers.ListField(child=serializers.CharField())


class FetchResultSerializer(serializers.Serializer):
    """Serialization of internal doglib response"""
    ref_files = serializers.ListField(child=_RefResourcesSerializer())
    description = serializers.CharField()
    license = serializers.CharField()
