from django.urls import path, include
from rest_framework import routers

from .views import ProtectedFileCreateView, ProtectedUrlCreateView, ProtectedFormView

from .api.views import (
    ProtectedFileCreate,
    ProtectedUrlCreate,
    ProtectedItemRetrieve,
    ProtectedItemStats,
)


router = routers.DefaultRouter()
router.register(r"protect/file", ProtectedFileCreate)
router.register(r"protect/url", ProtectedUrlCreate)


urlpatterns = [
    # forms
    path("protect/file/", ProtectedFileCreateView.as_view(), name="protect_file"),
    path("protect/url/", ProtectedUrlCreateView.as_view(), name="protect_url"),
    path("protected/<str:token>", ProtectedFormView.as_view(), name="protected"),
    # rest
    path(
        "api/protected/stats",
        ProtectedItemStats.as_view(),
        name="api_protected_stats",
    ),
    path(
        "api/protected/<str:token>",
        ProtectedItemRetrieve.as_view(),
        name="api_protected",
    ),
    path("api/", include(router.urls)),
]
