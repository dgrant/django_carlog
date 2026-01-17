from django.contrib.auth.models import User
from rest_framework import serializers

from trips.models import Car, Odometer, Trip


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ("url", "username", "email", "is_staff")
        extra_kwargs = {
            "url": {"view_name": "trips:user-detail"},
        }


class CarSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Car
        fields = (
            "url",
            "name",
        )
        extra_kwargs = {
            "url": {"view_name": "trips:car-detail"},
        }


class TripSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Trip
        fields = (
            "url",
            "date",
            "destination",
            "reason",
            "distance",
            "car",
        )
        extra_kwargs = {
            "url": {"view_name": "trips:trip-detail"},
            "car": {"view_name": "trips:car-detail"},
        }


class OdometerSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Odometer
        fields = (
            "url",
            "date",
            "car",
            "km",
        )
        extra_kwargs = {
            "url": {"view_name": "trips:odometer-detail"},
            "car": {"view_name": "trips:car-detail"},
        }
