"""
E2E tests for the REST API endpoints.
"""

from __future__ import annotations

from decimal import Decimal
from typing import TYPE_CHECKING

from django.utils import timezone

import pytest
from playwright.sync_api import expect

from trips.models import Car, Odometer, Trip


if TYPE_CHECKING:
    from playwright.sync_api import Page


@pytest.fixture
def sample_data(db):
    """Create sample data for API testing."""
    car = Car.objects.create(name="E2E Test Car")

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

    def test_api_root_accessible(self, page: Page, live_server):
        """Test that the API root is accessible."""
        page.goto(f"{live_server.url}/trips/api/")
        # DRF browsable API should load - check for heading specifically
        expect(page.locator("h1:has-text('Api Root')")).to_be_visible()

    def test_cars_api_lists_cars(self, page: Page, live_server, sample_data):
        """Test that cars API lists cars in browsable API."""
        page.goto(f"{live_server.url}/trips/api/cars/")
        expect(page.locator("h1:has-text('Car List')")).to_be_visible()
        expect(page.locator(f"text={sample_data['car'].name}")).to_be_visible()

    def test_trips_api_lists_trips(self, page: Page, live_server, sample_data):
        """Test that trips API lists trips in browsable API."""
        page.goto(f"{live_server.url}/trips/api/trips/")
        expect(page.locator("h1:has-text('Trip List')")).to_be_visible()
        expect(page.locator("text=E2E Destination")).to_be_visible()

    def test_odometers_api_lists_odometers(self, page: Page, live_server, sample_data):
        """Test that odometers API lists odometer readings."""
        page.goto(f"{live_server.url}/trips/api/odometers/")
        expect(page.locator("h1:has-text('Odometer List')")).to_be_visible()

    def test_car_detail_page(self, page: Page, live_server, sample_data):
        """Test viewing a specific car's detail page."""
        car_id = sample_data["car"].pk
        page.goto(f"{live_server.url}/trips/api/cars/{car_id}/")
        expect(page.locator("h1:has-text('Car Instance')")).to_be_visible()
        expect(page.locator(f"text={sample_data['car'].name}")).to_be_visible()

    def test_trip_detail_page(self, page: Page, live_server, sample_data):
        """Test viewing a specific trip's detail page."""
        trip_id = sample_data["trip"].pk
        page.goto(f"{live_server.url}/trips/api/trips/{trip_id}/")
        expect(page.locator("h1:has-text('Trip Instance')")).to_be_visible()
        expect(page.locator("text=E2E Destination")).to_be_visible()
        expect(page.locator("text=E2E Testing")).to_be_visible()


@pytest.mark.django_db(transaction=True)
class TestAPINavigation:
    """E2E tests for API navigation and pagination."""

    def test_navigate_from_root_to_cars(self, page: Page, live_server):
        """Test navigating from API root to cars endpoint."""
        page.goto(f"{live_server.url}/trips/api/")

        # Click on cars link in the content area
        page.click("a[href$='/cars/']")
        expect(page).to_have_url(f"{live_server.url}/trips/api/cars/")
        expect(page.locator("h1:has-text('Car List')")).to_be_visible()

    def test_navigate_from_root_to_trips(self, page: Page, live_server):
        """Test navigating from API root to trips endpoint."""
        page.goto(f"{live_server.url}/trips/api/")

        # Click on trips link - use the one ending with /trips/ exactly
        page.click("a[href$='/api/trips/']")
        expect(page).to_have_url(f"{live_server.url}/trips/api/trips/")
        expect(page.locator("h1:has-text('Trip List')")).to_be_visible()
