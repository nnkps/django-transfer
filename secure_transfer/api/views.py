from rest_framework import viewsets, status, views, permissions, mixins
from rest_framework.decorators import action
from rest_framework.response import Response

from .serializers import ProtectedItemSerializer
from ..models import ProtectedItem
