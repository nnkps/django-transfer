from django.contrib.auth.models import User
from rest_framework import serializers

from ..models import ProtectedUrl, ProtectedFile, ProtectedItem


class ProtectedUrlSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProtectedUrl
        fields = ["url"]


class ProtectedFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProtectedFile
        fields = ["uploaded_file"]


class ProtectedItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProtectedItem
        fields = ["password"]
