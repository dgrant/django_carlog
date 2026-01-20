"""
E2E tests for the REST API endpoints.
"""

from decimal import Decimal

from django.contrib.auth.models import User

import pytest
from playwright.sync_api import Page, expect

from trips.models import Car, Odometer, Trip


@pytest.fixture
def test_user(db):
    """Create a test user for authentication."""
    return User.objects.create_user(username="e2euser", email="e2e@test.com", password="e2epass123")


@pytest.fixture
def authenticated_page(page: Page, live_server, test_user):
    """Create an authenticated page by logging in."""
    # Go to login page and authenticate (allauth uses email)
    page.goto(f"{live_server.url}/accounts/login/")
    page.fill("input[name='login']", "e2e@test.com")
    page.fill("input[name='password']", "e2epass123")
    page.click("button[type='submit']")
    # Wait for redirect after login
    page.wait_for_url(f"{live_server.url}/**")
    return page


@pytest.fixture
def sample_data(test_user):
    """Create sample data for API testing."""
    car = Car.objects.create(name="E2E Test Car")
    from django.utils import timezone

    trip = Trip.objects.create(
        date=timezone.now().date(),
        destination="E2E Destination",
        reason="E2E Testing",
        distance=Decimal("50.0"),
        car=car,
    )
    odometer = Odometer.objects.create(
        date=timezone.now().date(),
        car=car,
        km=120000,
    )
    return {"car": car, "trip": trip, "odometer": odometer}


@pytest.mark.django_db(transaction=True)
class TestAPIEndpoints:
    """E2E tests for REST API using Playwright."""

    def test_api_root_accessible(self, authenticated_page: Page, live_server):
        """Test that the API root is accessible."""
        authenticated_page.goto(f"{live_server.url}/trips/api/")
        # DRF browsable API should load - check for heading specifically
        expect(authenticated_page.locator("h1:has-text('Api Root')")).to_be_visible()

    def test_cars_api_lists_cars(self, authenticated_page: Page, live_server, sample_data):
        """Test that cars API lists cars in browsable API."""
        authenticated_page.goto(f"{live_server.url}/trips/api/cars/")
        expect(authenticated_page.locator("h1:has-text('Car List')")).to_be_visible()
        expect(authenticated_page.locator(f"text={sample_data['car'].name}")).to_be_visible()

    def test_trips_api_lists_trips(self, authenticated_page: Page, live_server, sample_data):
        """Test that trips API lists trips in browsable API."""
        authenticated_page.goto(f"{live_server.url}/trips/api/trips/")
        expect(authenticated_page.locator("h1:has-text('Trip List')")).to_be_visible()
        expect(authenticated_page.locator("text=E2E Destination")).to_be_visible()

    def test_odometers_api_lists_odometers(self, authenticated_page: Page, live_server, sample_data):
        """Test that odometers API lists odometer readings."""
        authenticated_page.goto(f"{live_server.url}/trips/api/odometers/")
        expect(authenticated_page.locator("h1:has-text('Odometer List')")).to_be_visible()

    def test_car_detail_page(self, authenticated_page: Page, live_server, sample_data):
        """Test viewing a specific car's detail page."""
        car_id = sample_data["car"].pk
        authenticated_page.goto(f"{live_server.url}/trips/api/cars/{car_id}/")
        expect(authenticated_page.locator("h1:has-text('Car Instance')")).to_be_visible()
        # Use first() to handle DRF showing data in multiple places
        expect(authenticated_page.locator(f"text={sample_data['car'].name}").first).to_be_visible()

    def test_trip_detail_page(self, authenticated_page: Page, live_server, sample_data):
        """Test viewing a specific trip's detail page."""
        trip_id = sample_data["trip"].pk
        authenticated_page.goto(f"{live_server.url}/trips/api/trips/{trip_id}/")
        expect(authenticated_page.locator("h1:has-text('Trip Instance')")).to_be_visible()
        # Use first() to handle DRF showing data in multiple places
        expect(authenticated_page.locator("text=E2E Destination").first).to_be_visible()
        expect(authenticated_page.locator("text=E2E Testing").first).to_be_visible()


@pytest.mark.django_db(transaction=True)
class TestAPINavigation:
    """E2E tests for API navigation and pagination."""

    def test_navigate_from_root_to_cars(self, authenticated_page: Page, live_server):
        """Test navigating from API root to cars endpoint."""
        authenticated_page.goto(f"{live_server.url}/trips/api/")

        # Click on cars link in the content area
        authenticated_page.click("a[href$='/cars/']")
        expect(authenticated_page).to_have_url(f"{live_server.url}/trips/api/cars/")
        expect(authenticated_page.locator("h1:has-text('Car List')")).to_be_visible()

    def test_navigate_from_root_to_trips(self, authenticated_page: Page, live_server):
        """Test navigating from API root to trips endpoint."""
        authenticated_page.goto(f"{live_server.url}/trips/api/")

        # Click on trips link - use the one ending with /trips/ exactly
        authenticated_page.click("a[href$='/api/trips/']")
        expect(authenticated_page).to_have_url(f"{live_server.url}/trips/api/trips/")
        expect(authenticated_page.locator("h1:has-text('Trip List')")).to_be_visible()
