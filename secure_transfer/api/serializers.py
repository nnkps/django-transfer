from django.contrib.auth.models import User
from rest_framework import serializers

from ..models import ProtectedItem


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "email", "is_staff")


class ProtectedItemSerializer(serializers.ModelSerializer):
    token = serializers.CharField(read_only=True)

    class Meta:
        model = ProtectedItem
        fields = ("id", "token", "owner")
