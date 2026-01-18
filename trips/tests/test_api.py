"""Unit tests for trips API endpoints."""

from decimal import Decimal

import pytest
from rest_framework import status
from rest_framework.test import APIClient

from trips.models import Car, Odometer, Trip


@pytest.fixture
def api_client():
    """Create an API client for testing."""
    return APIClient()


@pytest.fixture
def sample_car():
    """Create a sample car for testing."""
    return Car.objects.create(name="API Test Car")


@pytest.mark.django_db
class TestCarAPI:
    """Tests for the Car API endpoints."""

    def test_list_cars(self, api_client, sample_car):
        """Test listing all cars."""
        response = api_client.get("/trips/api/cars/")
        assert response.status_code == status.HTTP_200_OK
        assert "results" in response.data
        assert len(response.data["results"]) >= 1

    def test_get_car_detail(self, api_client, sample_car):
        """Test getting a single car."""
        response = api_client.get(f"/trips/api/cars/{sample_car.pk}/")
        assert response.status_code == status.HTTP_200_OK
        assert response.data["name"] == "API Test Car"

    def test_car_not_found(self, api_client):
        """Test getting a non-existent car."""
        response = api_client.get("/trips/api/cars/99999/")
        assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
class TestTripAPI:
    """Tests for the Trip API endpoints."""

    @pytest.fixture
    def sample_trip(self, sample_car):
        """Create a sample trip for testing."""
        from django.utils import timezone

        return Trip.objects.create(
            date=timezone.now().date(),
            destination="Test Destination",
            reason="Test Reason",
            distance=Decimal("25.5"),
            car=sample_car,
        )

    def test_list_trips(self, api_client, sample_trip):
        """Test listing all trips."""
        response = api_client.get("/trips/api/trips/")
        assert response.status_code == status.HTTP_200_OK
        assert "results" in response.data
        assert len(response.data["results"]) >= 1

    def test_get_trip_detail(self, api_client, sample_trip):
        """Test getting a single trip."""
        response = api_client.get(f"/trips/api/trips/{sample_trip.pk}/")
        assert response.status_code == status.HTTP_200_OK
        assert response.data["destination"] == "Test Destination"
        assert response.data["reason"] == "Test Reason"
        assert Decimal(response.data["distance"]) == Decimal("25.5")

    def test_filter_trips_by_car(self, api_client, sample_trip, sample_car):
        """Test filtering trips by car."""
        response = api_client.get(f"/trips/api/trips/?car={sample_car.pk}")
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["results"]) >= 1


@pytest.mark.django_db
class TestOdometerAPI:
    """Tests for the Odometer API endpoints."""

    @pytest.fixture
    def sample_odometer(self, sample_car):
        """Create a sample odometer reading for testing."""
        from django.utils import timezone

        return Odometer.objects.create(
            date=timezone.now().date(),
            car=sample_car,
            km=100000,
        )

    def test_list_odometers(self, api_client, sample_odometer):
        """Test listing all odometer readings."""
        response = api_client.get("/trips/api/odometers/")
        assert response.status_code == status.HTTP_200_OK
        assert "results" in response.data
        assert len(response.data["results"]) >= 1

    def test_get_odometer_detail(self, api_client, sample_odometer):
        """Test getting a single odometer reading."""
        response = api_client.get(f"/trips/api/odometers/{sample_odometer.pk}/")
        assert response.status_code == status.HTTP_200_OK
        assert response.data["km"] == 100000
