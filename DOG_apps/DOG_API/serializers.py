from rest_framework import serializers


class SniffSerializer(serializers.Serializer):
    """Registered repository serializer"""
    repo_name = serializers.CharField()
    host_url = serializers.CharField()


class FetchSerializer(serializers.Serializer):
    """DOGlib result serializer"""
    ref_resources = serializers.ListSerializer()
    description = serializers.CharField()
    license = serializers.CharField()


class PIDSerializer(serializers.Serializer):
    """Registered repository serializer"""
    pid = serializers.CharField()
