"""Unit tests for trips models."""

from datetime import timedelta
from decimal import Decimal

from django.db import IntegrityError
from django.utils import timezone

import pytest

from trips.models import Car, Odometer, Trip


@pytest.mark.django_db
class TestCarModel:
    """Tests for the Car model."""

    def test_create_car(self):
        """Test creating a car."""
        car = Car.objects.create(name="Tesla Model 3")
        assert car.name == "Tesla Model 3"
        assert car.pk is not None

    def test_car_str(self):
        """Test car string representation."""
        car = Car.objects.create(name="Honda Civic")
        assert str(car) == "Honda Civic"

    def test_car_unique_name(self):
        """Test that car names must be unique."""
        Car.objects.create(name="Toyota Camry")
        with pytest.raises(IntegrityError):
            Car.objects.create(name="Toyota Camry")

    def test_car_ordering(self):
        """Test that cars are ordered by name."""
        Car.objects.create(name="Zebra Car")
        Car.objects.create(name="Alpha Car")
        Car.objects.create(name="Middle Car")

        cars = list(Car.objects.all())
        assert cars[0].name == "Alpha Car"
        assert cars[1].name == "Middle Car"
        assert cars[2].name == "Zebra Car"


@pytest.mark.django_db
class TestTripModel:
    """Tests for the Trip model."""

    @pytest.fixture
    def car(self):
        """Create a car for testing."""
        return Car.objects.create(name="Test Car")

    def test_create_trip(self, car):
        """Test creating a trip."""
        trip = Trip.objects.create(
            date=timezone.now().date(),
            destination="Downtown",
            reason="Work",
            distance=Decimal("15.5"),
            car=car,
        )
        assert trip.pk is not None
        assert trip.destination == "Downtown"
        assert trip.reason == "Work"
        assert trip.distance == Decimal("15.5")
        assert trip.car == car

    def test_trip_str(self, car):
        """Test trip string representation."""
        today = timezone.now().date()
        trip = Trip.objects.create(
            date=today,
            destination="Airport",
            reason="Travel",
            distance=Decimal("45.0"),
            car=car,
        )
        expected = f"{today} to Airport for Travel (45.0 km)"
        assert str(trip) == expected

    def test_trip_ordering(self, car):
        """Test that trips are ordered by date descending."""
        today = timezone.now().date()
        yesterday = today - timedelta(days=1)
        tomorrow = today + timedelta(days=1)

        Trip.objects.create(date=yesterday, destination="A", reason="R", distance=Decimal(10), car=car)
        Trip.objects.create(date=tomorrow, destination="B", reason="R", distance=Decimal(10), car=car)
        Trip.objects.create(date=today, destination="C", reason="R", distance=Decimal(10), car=car)

        trips = list(Trip.objects.all())
        assert trips[0].date == tomorrow
        assert trips[1].date == today
        assert trips[2].date == yesterday


@pytest.mark.django_db
class TestOdometerModel:
    """Tests for the Odometer model."""

    @pytest.fixture
    def car(self):
        """Create a car for testing."""
        return Car.objects.create(name="Odometer Test Car")

    def test_create_odometer(self, car):
        """Test creating an odometer reading."""
        odometer = Odometer.objects.create(
            date=timezone.now().date(),
            car=car,
            km=50000,
        )
        assert odometer.pk is not None
        assert odometer.km == 50000
        assert odometer.car == car

    def test_odometer_str(self, car):
        """Test odometer string representation."""
        today = timezone.now().date()
        odometer = Odometer.objects.create(
            date=today,
            car=car,
            km=75000,
        )
        expected = f"{today} 75000 km ({car})"
        assert str(odometer) == expected

    def test_odometer_ordering(self, car):
        """Test that odometer readings are ordered by date descending."""
        today = timezone.now().date()
        yesterday = today - timedelta(days=1)

        Odometer.objects.create(date=yesterday, car=car, km=49000)
        Odometer.objects.create(date=today, car=car, km=50000)

        readings = list(Odometer.objects.all())
        assert readings[0].date == today
        assert readings[1].date == yesterday
