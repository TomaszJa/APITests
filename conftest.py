from typing import Any, Generator

import pytest
from playwright.sync_api import Playwright, APIRequestContext

"""
Defining a shared context can help with scaling the applicating without duplication of code.
"""
@pytest.fixture(scope="session")
def api_context(
    playwright: Playwright,
    base_url: str  # Automatically fetched from pytest.ini or --base-url CLI flag
) -> Generator[APIRequestContext, Any, None]:
    """
    Session-scoped API request context shared across all test files.
    """
    # Create request context with global configuration
    request_context = playwright.request.new_context(
        base_url=base_url,
        extra_http_headers={
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
    )

    yield request_context

    # Tear down session after all tests finish
    request_context.dispose()