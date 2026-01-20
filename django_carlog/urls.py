from django.contrib import admin
from django.http import JsonResponse
from django.urls import include, path

from trips.views import HomeView


def health_check(request):
    """Health check endpoint for Docker and load balancers."""
    return JsonResponse({"status": "ok"})


urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("admin/", admin.site.urls),
    path("trips/", include("trips.urls")),
    path("accounts/", include("allauth.urls")),
    path("health/", health_check, name="health-check"),
]
