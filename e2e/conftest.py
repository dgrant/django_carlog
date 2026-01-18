"""
Playwright E2E test configuration.
"""

import os

import pytest


# Allow Django to run synchronous database operations in async contexts
# This is required for pytest-playwright E2E tests which run in an async context
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    """Configure browser context for tests."""
    return {
        **browser_context_args,
        "viewport": {"width": 1280, "height": 720},
    }
