"""Unit tests for trips views (template views)."""

from datetime import date
from decimal import Decimal

from django.contrib.auth.models import User
from django.test import Client
from django.urls import reverse

import pytest

from trips.models import Car, Odometer, Trip


@pytest.fixture
def user(db):
    """Create a test user."""
    return User.objects.create_user(username="testuser", password="testpass123")


@pytest.fixture
def client(user):
    """Create an authenticated test client."""
    c = Client()
    c.login(username="testuser", password="testpass123")
    return c


@pytest.fixture
def sample_car(db):
    """Create a sample car."""
    return Car.objects.create(name="Test Car")


@pytest.fixture
def sample_trip(db, sample_car):
    """Create a sample trip."""
    return Trip.objects.create(
        date=date(2025, 1, 15),
        destination="Client Office",
        reason="Business",
        distance=Decimal("25.5"),
        car=sample_car,
    )


@pytest.fixture
def sample_odometer(db, sample_car):
    """Create a sample odometer reading."""
    return Odometer.objects.create(
        date=date(2025, 1, 1),
        car=sample_car,
        km=50000,
    )


@pytest.fixture
def anonymous_client():
    """Create an unauthenticated test client."""
    return Client()


@pytest.mark.django_db
class TestHomeView:
    """Tests for the Home view (root page)."""

    def test_home_redirects_unauthenticated_to_login(self, anonymous_client):
        """Test that unauthenticated users are redirected to login."""
        response = anonymous_client.get(reverse("home"))
        assert response.status_code == 302
        assert "accounts/login" in response.url

    def test_home_redirects_authenticated_to_dashboard(self, client, user):
        """Test that authenticated users are redirected to dashboard."""
        client.login(username="testuser", password="testpass123")
        response = client.get(reverse("home"))
        assert response.status_code == 302
        assert response.url == reverse("trips:dashboard")


@pytest.mark.django_db
class TestDashboardView:
    """Tests for the Dashboard view."""

    def test_dashboard_renders(self, client):
        """Test that dashboard renders successfully."""
        response = client.get(reverse("trips:dashboard"))
        assert response.status_code == 200

    def test_dashboard_context_has_stats(self, client, sample_trip):
        """Test that dashboard has statistics in context."""
        response = client.get(reverse("trips:dashboard"))
        assert "current_year" in response.context
        assert "trips_this_year" in response.context
        assert "total_distance_year" in response.context
        assert "recent_trips" in response.context

    def test_dashboard_shows_recent_trips(self, client, sample_trip):
        """Test that dashboard shows recent trips."""
        response = client.get(reverse("trips:dashboard"))
        assert sample_trip in response.context["recent_trips"]


@pytest.mark.django_db
class TestTripListView:
    """Tests for the Trip List view."""

    def test_trip_list_renders(self, client):
        """Test that trip list renders successfully."""
        response = client.get(reverse("trips:trip_list"))
        assert response.status_code == 200

    def test_trip_list_shows_trips(self, client, sample_trip):
        """Test that trip list shows trips."""
        response = client.get(reverse("trips:trip_list"))
        assert sample_trip in response.context["trips"]

    def test_trip_list_filter_by_year(self, client, sample_trip):
        """Test filtering trips by year."""
        response = client.get(reverse("trips:trip_list"), {"year": "2025"})
        assert response.status_code == 200
        assert sample_trip in response.context["trips"]

    def test_trip_list_filter_by_car(self, client, sample_trip, sample_car):
        """Test filtering trips by car."""
        response = client.get(reverse("trips:trip_list"), {"car": str(sample_car.pk)})
        assert response.status_code == 200
        assert sample_trip in response.context["trips"]

    def test_trip_list_filter_by_reason(self, client, sample_trip):
        """Test filtering trips by reason."""
        response = client.get(reverse("trips:trip_list"), {"reason": "Business"})
        assert response.status_code == 200
        assert sample_trip in response.context["trips"]

    def test_trip_list_context_has_filters(self, client, sample_trip):
        """Test that trip list has filter options in context."""
        response = client.get(reverse("trips:trip_list"))
        assert "years" in response.context
        assert "cars" in response.context
        assert "reasons" in response.context
        assert "total_distance" in response.context


@pytest.mark.django_db
class TestTripCreateView:
    """Tests for the Trip Create view."""

    def test_trip_create_renders(self, client, sample_car):
        """Test that trip create form renders."""
        response = client.get(reverse("trips:trip_add"))
        assert response.status_code == 200

    def test_trip_create_context(self, client, sample_car):
        """Test that trip create has correct context."""
        response = client.get(reverse("trips:trip_add"))
        assert "cars" in response.context
        assert "today" in response.context

    def test_trip_create_with_prefill(self, client, sample_car):
        """Test trip create with prefilled values."""
        response = client.get(
            reverse("trips:trip_add"),
            {"destination": "Client Office", "reason": "Business"},
        )
        assert response.status_code == 200
        assert response.context["prefill_destination"] == "Client Office"
        assert response.context["prefill_reason"] == "Business"

    def test_trip_create_post(self, client, sample_car):
        """Test creating a trip via POST."""
        response = client.post(
            reverse("trips:trip_add"),
            {
                "date": "2025-01-20",
                "destination": "Downtown",
                "reason": "Business",
                "distance": "30.0",
                "car": sample_car.pk,
            },
        )
        assert response.status_code == 302  # Redirect on success
        assert Trip.objects.filter(destination="Downtown").exists()


@pytest.mark.django_db
class TestTripQuickAddView:
    """Tests for the Trip Quick Add view."""

    def test_trip_quick_add_renders(self, client, sample_car):
        """Test that quick add form renders."""
        response = client.get(reverse("trips:trip_add_quick"))
        assert response.status_code == 200

    def test_trip_quick_add_with_params(self, client, sample_car):
        """Test quick add with URL parameters."""
        response = client.get(
            reverse("trips:trip_add_quick"),
            {"destination": "Client Office", "reason": "Business"},
        )
        assert response.status_code == 200


@pytest.mark.django_db
class TestTripUpdateView:
    """Tests for the Trip Update view."""

    def test_trip_update_renders(self, client, sample_trip):
        """Test that trip update form renders."""
        response = client.get(reverse("trips:trip_edit", args=[sample_trip.pk]))
        assert response.status_code == 200

    def test_trip_update_post(self, client, sample_trip, sample_car):
        """Test updating a trip via POST."""
        response = client.post(
            reverse("trips:trip_edit", args=[sample_trip.pk]),
            {
                "date": "2025-01-16",
                "destination": "Updated Dest",
                "reason": "Updated Reason",
                "distance": "35.0",
                "car": sample_car.pk,
            },
        )
        assert response.status_code == 302  # Redirect on success
        sample_trip.refresh_from_db()
        assert sample_trip.destination == "Updated Dest"


@pytest.mark.django_db
class TestTripDeleteView:
    """Tests for the Trip Delete view."""

    def test_trip_delete_renders(self, client, sample_trip):
        """Test that trip delete confirmation renders."""
        response = client.get(reverse("trips:trip_delete", args=[sample_trip.pk]))
        assert response.status_code == 200

    def test_trip_delete_post(self, client, sample_trip):
        """Test deleting a trip via POST."""
        trip_pk = sample_trip.pk
        response = client.post(reverse("trips:trip_delete", args=[trip_pk]))
        assert response.status_code == 302  # Redirect on success
        assert not Trip.objects.filter(pk=trip_pk).exists()


@pytest.mark.django_db
class TestCRAReportView:
    """Tests for the CRA Report view."""

    def test_cra_report_renders(self, client):
        """Test that CRA report renders successfully."""
        response = client.get(reverse("trips:cra_report"))
        assert response.status_code == 200

    def test_cra_report_with_year(self, client, sample_trip):
        """Test CRA report with year parameter."""
        response = client.get(reverse("trips:cra_report"), {"year": "2025"})
        assert response.status_code == 200
        assert response.context["selected_year"] == 2025

    def test_cra_report_context(self, client, sample_trip):
        """Test that CRA report has correct context."""
        response = client.get(reverse("trips:cra_report"), {"year": "2025"})
        assert "years" in response.context
        assert "trips" in response.context
        assert "trips_summary" in response.context
        assert "monthly_data" in response.context
        assert "cra_rate" in response.context
        assert "estimated_deduction" in response.context

    def test_cra_report_with_odometer(self, client, sample_trip, sample_odometer):
        """Test CRA report includes odometer data."""
        # Create end-of-year odometer reading
        Odometer.objects.create(
            date=date(2025, 12, 31),
            car=sample_trip.car,
            km=60000,
        )
        response = client.get(reverse("trips:cra_report"), {"year": "2025"})
        assert response.status_code == 200
        assert "car_odometer_data" in response.context

    def test_cra_report_empty_year(self, client):
        """Test CRA report with no trips in year."""
        response = client.get(reverse("trips:cra_report"), {"year": "2020"})
        assert response.status_code == 200


@pytest.mark.django_db
class TestCarListView:
    """Tests for the Car List view."""

    def test_car_list_renders(self, client):
        """Test that car list renders successfully."""
        response = client.get(reverse("trips:car_list"))
        assert response.status_code == 200

    def test_car_list_shows_cars(self, client, sample_car):
        """Test that car list shows cars."""
        response = client.get(reverse("trips:car_list"))
        assert sample_car.name in str(response.content)

    def test_car_list_shows_trip_count(self, client, sample_trip):
        """Test that car list shows trip count per car."""
        response = client.get(reverse("trips:car_list"))
        cars = response.context["cars"]
        car = cars.get(pk=sample_trip.car.pk)
        assert car.trip_count == 1

    def test_car_list_shows_total_distance(self, client, sample_trip):
        """Test that car list shows total distance per car."""
        response = client.get(reverse("trips:car_list"))
        cars = response.context["cars"]
        car = cars.get(pk=sample_trip.car.pk)
        assert car.total_distance == sample_trip.distance


@pytest.mark.django_db
class TestCarCreateView:
    """Tests for the Car Create view."""

    def test_car_create_renders(self, client):
        """Test that car create form renders."""
        response = client.get(reverse("trips:car_add"))
        assert response.status_code == 200

    def test_car_create_post(self, client):
        """Test creating a car via POST."""
        response = client.post(
            reverse("trips:car_add"),
            {"name": "New Test Car"},
        )
        assert response.status_code == 302  # Redirect on success
        assert Car.objects.filter(name="New Test Car").exists()

    def test_car_create_duplicate_name(self, client, sample_car):
        """Test creating a car with duplicate name fails."""
        response = client.post(
            reverse("trips:car_add"),
            {"name": sample_car.name},
        )
        assert response.status_code == 200  # Re-renders form with errors
        assert Car.objects.filter(name=sample_car.name).count() == 1


@pytest.mark.django_db
class TestCarUpdateView:
    """Tests for the Car Update view."""

    def test_car_update_renders(self, client, sample_car):
        """Test that car update form renders."""
        response = client.get(reverse("trips:car_edit", args=[sample_car.pk]))
        assert response.status_code == 200

    def test_car_update_post(self, client, sample_car):
        """Test updating a car via POST."""
        response = client.post(
            reverse("trips:car_edit", args=[sample_car.pk]),
            {"name": "Updated Car Name"},
        )
        assert response.status_code == 302  # Redirect on success
        sample_car.refresh_from_db()
        assert sample_car.name == "Updated Car Name"


@pytest.mark.django_db
class TestCarDeleteView:
    """Tests for the Car Delete view."""

    def test_car_delete_renders(self, client, sample_car):
        """Test that car delete confirmation renders."""
        response = client.get(reverse("trips:car_delete", args=[sample_car.pk]))
        assert response.status_code == 200

    def test_car_delete_shows_trip_count(self, client, sample_trip):
        """Test that car delete shows trip count warning."""
        response = client.get(reverse("trips:car_delete", args=[sample_trip.car.pk]))
        assert response.context["trip_count"] == 1

    def test_car_delete_post(self, client, sample_car):
        """Test deleting a car via POST."""
        car_pk = sample_car.pk
        response = client.post(reverse("trips:car_delete", args=[car_pk]))
        assert response.status_code == 302  # Redirect on success
        assert not Car.objects.filter(pk=car_pk).exists()

    def test_car_delete_cascades_trips(self, client, sample_trip):
        """Test that deleting a car also deletes associated trips."""
        car_pk = sample_trip.car.pk
        trip_pk = sample_trip.pk
        response = client.post(reverse("trips:car_delete", args=[car_pk]))
        assert response.status_code == 302
        assert not Car.objects.filter(pk=car_pk).exists()
        assert not Trip.objects.filter(pk=trip_pk).exists()
