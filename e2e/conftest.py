"""
Playwright E2E test configuration.
"""

import pytest


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    """Configure browser context for tests."""
    return {
        **browser_context_args,
        "viewport": {"width": 1280, "height": 720},
    }


@pytest.fixture
def base_url(live_server):
    """Get the base URL from the live server fixture."""
    return live_server.url
