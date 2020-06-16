from django.contrib.auth.models import User
from rest_framework import serializers

from trips.models import Car, Odometer, Trip


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ("url", "username", "email", "is_staff")


class CarSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Car
        fields = (
            "url",
            "name",
        )


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


class OdometerSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Odometer
        fields = (
            "url",
            "date",
            "car",
            "km",
        )
