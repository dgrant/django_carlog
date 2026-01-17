"""Unit tests for trips serializers."""

import pytest
from decimal import Decimal
from django.utils import timezone

from trips.models import Car, Trip, Odometer
from trips.serializers import CarSerializer, TripSerializer, OdometerSerializer


@pytest.mark.django_db
class TestCarSerializer:
    """Tests for the Car serializer."""

    def test_serialize_car(self):
        """Test serializing a car."""
        car = Car.objects.create(name="Serializer Test Car")
        serializer = CarSerializer(car, context={"request": None})
        assert serializer.data["name"] == "Serializer Test Car"

    def test_car_fields(self):
        """Test that car serializer has expected fields."""
        car = Car.objects.create(name="Fields Test Car")
        serializer = CarSerializer(car, context={"request": None})
        assert "name" in serializer.data


@pytest.mark.django_db
class TestTripSerializer:
    """Tests for the Trip serializer."""

    @pytest.fixture
    def car(self):
        """Create a car for testing."""
        return Car.objects.create(name="Trip Serializer Car")

    def test_serialize_trip(self, car):
        """Test serializing a trip."""
        trip = Trip.objects.create(
            date=timezone.now().date(),
            destination="Serialize Dest",
            reason="Serialize Reason",
            distance=Decimal("30.0"),
            car=car,
        )
        serializer = TripSerializer(trip, context={"request": None})
        assert serializer.data["destination"] == "Serialize Dest"
        assert serializer.data["reason"] == "Serialize Reason"
        assert Decimal(serializer.data["distance"]) == Decimal("30.0")

    def test_trip_fields(self, car):
        """Test that trip serializer has expected fields."""
        trip = Trip.objects.create(
            date=timezone.now().date(),
            destination="Fields Dest",
            reason="Fields Reason",
            distance=Decimal("20.0"),
            car=car,
        )
        serializer = TripSerializer(trip, context={"request": None})
        expected_fields = ["date", "destination", "reason", "distance", "car"]
        for field in expected_fields:
            assert field in serializer.data


@pytest.mark.django_db
class TestOdometerSerializer:
    """Tests for the Odometer serializer."""

    @pytest.fixture
    def car(self):
        """Create a car for testing."""
        return Car.objects.create(name="Odometer Serializer Car")

    def test_serialize_odometer(self, car):
        """Test serializing an odometer reading."""
        odometer = Odometer.objects.create(
            date=timezone.now().date(),
            car=car,
            km=80000,
        )
        serializer = OdometerSerializer(odometer, context={"request": None})
        assert serializer.data["km"] == 80000

    def test_odometer_fields(self, car):
        """Test that odometer serializer has expected fields."""
        odometer = Odometer.objects.create(
            date=timezone.now().date(),
            car=car,
            km=90000,
        )
        serializer = OdometerSerializer(odometer, context={"request": None})
        expected_fields = ["date", "car", "km"]
        for field in expected_fields:
            assert field in serializer.data
