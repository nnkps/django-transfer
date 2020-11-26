from django.contrib import admin
from django.urls import path, include

from rest_framework import routers

# from secure_transfer.api.views import ProtectedItemViewSet

router = routers.DefaultRouter()
# router.register(r"protect", ProtectedItemViewSet)

urlpatterns = [
    path("api/", include(router.urls)),
    path("admin/", admin.site.urls),
    path("accounts/", include("rest_framework.urls")),
    path("", include("secure_transfer.urls")),
]
