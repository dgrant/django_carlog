from django.urls import include, path
from rest_framework import routers

from trips.views import CarViewSet, OdometerViewSet, TripViewSet, UserViewSet

router = routers.DefaultRouter()
router.register(r"users", UserViewSet)
router.register(r"cars", CarViewSet)
router.register(r"trips", TripViewSet)
router.register(r"odometers", OdometerViewSet)

urlpatterns = [
    path("api/", include(router.urls)),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
]
