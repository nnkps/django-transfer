from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("rest_framework.urls")),
    path("", include("secure_transfer.urls")),
]
