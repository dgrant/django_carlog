"""
E2E tests for the Django Admin interface.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from django.contrib.auth.models import User

import pytest
from playwright.sync_api import expect


if TYPE_CHECKING:
    from playwright.sync_api import Page


@pytest.fixture
def admin_user(db):
    """Create an admin user for testing."""
    user = User.objects.create_superuser(
        username="admin",
        email="admin@test.com",
        password="adminpassword123",
    )
    return user


@pytest.mark.django_db(transaction=True)
class TestAdminInterface:
    """E2E tests for Django Admin."""

    def test_admin_login_page_loads(self, page: Page, live_server):
        """Test that the admin login page loads correctly."""
        page.goto(f"{live_server.url}/admin/")
        expect(page).to_have_title("Log in | Django site admin")
        expect(page.locator("input[name='username']")).to_be_visible()
        expect(page.locator("input[name='password']")).to_be_visible()

    def test_admin_login_success(self, page: Page, live_server, admin_user):
        """Test successful admin login."""
        page.goto(f"{live_server.url}/admin/")

        # Fill in credentials
        page.fill("input[name='username']", "admin")
        page.fill("input[name='password']", "adminpassword123")
        page.click("input[type='submit']")

        # Should be redirected to admin dashboard
        expect(page).to_have_title("Site administration | Django site admin")
        expect(page.locator("text=Site administration")).to_be_visible()

    def test_admin_login_failure(self, page: Page, live_server, admin_user):
        """Test failed admin login with wrong password."""
        page.goto(f"{live_server.url}/admin/")

        # Fill in wrong credentials
        page.fill("input[name='username']", "admin")
        page.fill("input[name='password']", "wrongpassword")
        page.click("input[type='submit']")

        # Should show error message
        expect(page.locator(".errornote")).to_be_visible()

    def test_admin_can_view_cars(self, page: Page, live_server, admin_user):
        """Test that admin can view the cars list."""
        # Login first
        page.goto(f"{live_server.url}/admin/")
        page.fill("input[name='username']", "admin")
        page.fill("input[name='password']", "adminpassword123")
        page.click("input[type='submit']")

        # Navigate to cars
        page.click("text=Cars")
        expect(page).to_have_url(f"{live_server.url}/admin/trips/car/")
        expect(page.locator("text=Select car to change")).to_be_visible()

    def test_admin_can_view_trips(self, page: Page, live_server, admin_user):
        """Test that admin can view the trips list."""
        # Login first
        page.goto(f"{live_server.url}/admin/")
        page.fill("input[name='username']", "admin")
        page.fill("input[name='password']", "adminpassword123")
        page.click("input[type='submit']")

        # Navigate to trips - use the specific model link
        page.click("a[href='/admin/trips/trip/']")
        expect(page).to_have_url(f"{live_server.url}/admin/trips/trip/")
        expect(page.locator("text=Select trip to change")).to_be_visible()
