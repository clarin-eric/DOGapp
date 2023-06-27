"""Serializer classes for drf_spectacular OpenAPI 3.0 documentation"""
from rest_framework import serializers


class _RefResourcesSerializer(serializers.Serializer):
    resource_type = serializers.CharField()
    pid = serializers.ListField(child=serializers.CharField())


class FetchResultSerializer(serializers.Serializer):
    """Serialization of internal doglib response"""
    ref_files = serializers.ListField(child=_RefResourcesSerializer())
    description = serializers.CharField()
    license = serializers.CharField()
