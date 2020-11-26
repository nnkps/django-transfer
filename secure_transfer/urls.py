from django.urls import path, include

from .views import ProtectedFileCreateView, ProtectedUrlCreateView, ProtectedFormView

urlpatterns = [
    path("protect/file/", ProtectedFileCreateView.as_view(), name="protect_file"),
    path("protect/url/", ProtectedUrlCreateView.as_view(), name="protect_url"),
    path("protected/<str:token>", ProtectedFormView.as_view(), name="protected"),
]
