from django.db.models.functions import TruncDay
from django.db.models import Count
from django.db.models.expressions import Case, When, Value
from django.shortcuts import reverse


from rest_framework import viewsets, status, views, permissions, mixins, generics
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response


from ..models import ProtectedItem, ProtectedUrl, ProtectedFile
from .serializers import (
    ProtectedUrlSerializer,
    ProtectedFileSerializer,
    ProtectedItemSerializer,
)


class ProtectedItemCreate(mixins.CreateModelMixin, viewsets.GenericViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = ProtectedItem.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        item = serializer.save(owner=self.request.user)
        password = item.create_random_password()
        item.save()
        return Response(
            {
                "password": password,
                "link": reverse("api_protected", args=[item.token]),
            }
        )


class ProtectedUrlCreate(ProtectedItemCreate):
    serializer_class = ProtectedUrlSerializer


class ProtectedFileCreate(ProtectedItemCreate):
    serializer_class = ProtectedFileSerializer


class ProtectedItemRetrieve(generics.RetrieveAPIView):
    queryset = ProtectedItem.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = ProtectedItemSerializer
    lookup_field = "token"

    def retrieve(self, request, *args, **kwargs):
        item = self.get_object()
        if item.is_expired:
            raise PermissionDenied({"message": "link expired"})
        serializer = self.get_serializer(data=request.GET)
        serializer.is_valid(raise_exception=True)
        password = serializer["password"].value

        if not item.check_password(password):
            raise PermissionDenied({"message": "password incorrect"})

        item.count_correct_redirect()
        item.save()
        return item.get_response()


class ProtectedItemStats(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        items = (
            ProtectedItem.objects.annotate(
                is_link=Case(
                    When(protectedfile__isnull=True, then=Value("True")),
                    default=Value("False"),
                )
            )
            # .extra(select={"day": "TO_CHAR(created, 'YYYY-MM-DD')"})
            # .values("day", "is_link")
            # .order_by("day")
            # .annotate(available=Count("created"))
        )

        print(items)

        stats = []
        return Response({})
