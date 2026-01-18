from django.urls import include, path

from rest_framework import routers

from trips.views import (
    CarViewSet,
    CRAReportView,
    DashboardView,
    OdometerViewSet,
    TripCreateView,
    TripDeleteView,
    TripListView,
    TripQuickAddView,
    TripUpdateView,
    TripViewSet,
    UserViewSet,
)


app_name = "trips"

router = routers.DefaultRouter()
router.register(r"users", UserViewSet)
router.register(r"cars", CarViewSet)
router.register(r"trips", TripViewSet)
router.register(r"odometers", OdometerViewSet)

urlpatterns = [
    # Template views
    path("", DashboardView.as_view(), name="dashboard"),
    path("trips/", TripListView.as_view(), name="trip_list"),
    path("trips/add/", TripCreateView.as_view(), name="trip_add"),
    path("trips/add/quick/", TripQuickAddView.as_view(), name="trip_add_quick"),
    path("trips/<int:pk>/edit/", TripUpdateView.as_view(), name="trip_edit"),
    path("trips/<int:pk>/delete/", TripDeleteView.as_view(), name="trip_delete"),
    path("reports/cra/", CRAReportView.as_view(), name="cra_report"),
    # API views
    path("api/", include(router.urls)),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
]
