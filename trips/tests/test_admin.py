"""Unit tests for trips admin."""

from django.contrib.admin.sites import AdminSite
from django.contrib.auth.models import User
from django.test import RequestFactory

import pytest

from trips.admin import CarAdmin, TripInline
from trips.models import Car, Trip


@pytest.fixture
def site():
    """Create admin site."""
    return AdminSite()


@pytest.fixture
def request_factory():
    """Create request factory."""
    return RequestFactory()


@pytest.fixture
def admin_user(db):
    """Create an admin user."""
    return User.objects.create_superuser(
        username="admin",
        email="admin@test.com",
        password="adminpass",
    )


@pytest.mark.django_db
class TestTripInline:
    """Tests for the TripInline admin."""

    def test_get_queryset_returns_none(self, site, request_factory, admin_user):
        """Test that TripInline.get_queryset returns empty queryset."""
        car = Car.objects.create(name="Admin Test Car")
        Trip.objects.create(
            date="2025-01-15",
            destination="Test Dest",
            reason="Test Reason",
            distance="10.0",
            car=car,
        )

        inline = TripInline(Car, site)

        request = request_factory.get("/admin/trips/car/")
        request.user = admin_user
        queryset = inline.get_queryset(request)

        # Should return empty queryset even though trips exist
        assert queryset.count() == 0


@pytest.mark.django_db
class TestCarAdmin:
    """Tests for the CarAdmin."""

    def test_car_admin_has_trip_inline(self, site):
        """Test that CarAdmin has TripInline."""
        car_admin = CarAdmin(Car, site)
        assert TripInline in car_admin.inlines
