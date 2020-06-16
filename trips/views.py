from django.contrib.auth.models import User
from django_filters import rest_framework as filters
from rest_framework import viewsets

from trips.models import Car, Odometer, Trip
from trips.serializers import (
    CarSerializer,
    OdometerSerializer,
    TripSerializer,
    UserSerializer,
)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class CarViewSet(viewsets.ModelViewSet):
    queryset = Car.objects.all()
    serializer_class = CarSerializer


class TripFilter(filters.FilterSet):
    date = filters.DateFromToRangeFilter(field_name="date")

    class Meta:
        model = Trip
        fields = ["car", "date"]


class TripViewSet(viewsets.ModelViewSet):
    queryset = Trip.objects.all()
    serializer_class = TripSerializer
    # filterset_fields = ["car", "date"]
    filterset_class = TripFilter


class OdometerViewSet(viewsets.ModelViewSet):
    queryset = Odometer.objects.all()
    serializer_class = OdometerSerializer
