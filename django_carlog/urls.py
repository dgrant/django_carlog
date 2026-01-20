from django.contrib import admin
from django.urls import include, path

from trips.views import HomeView


urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("admin/", admin.site.urls),
    path("trips/", include("trips.urls")),
    path("accounts/", include("allauth.urls")),
]
