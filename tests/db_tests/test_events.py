import os
import unittest

import pytest
from deepdiff import DeepDiff
from httpx import ASGITransport, AsyncClient

from src.config import get_settings
from src.main import app
from tests.db_tests.conftest import load_db_fixture

DOCKER_CONTAINER = os.getenv("DOCKER_CONTAINER", "False").lower() == "true"
settings = get_settings()
api_prefix = settings.api_prefix


@unittest.skipUnless(DOCKER_CONTAINER, "Don't run this test locally")
@pytest.mark.asyncio(loop_scope="session")
@pytest.mark.parametrize(
    "method, url, request_kwargs, response_code, response_data, response_diff_kwargs",
    [
        ("GET", f"{api_prefix}/events", {}, 200, "all_events", {}),
        ("DELETE", f"{api_prefix}/events/1", {}, 200, "delete_event_1", {}),
        (
            "POST",
            f"{api_prefix}/events",
            {
                "json": {
                    "name": "A Brand New Event",
                    "description": "A Brand New Event Description",
                    "starts_at": "2022-01-01T00:00:00Z",
                    "duration": 60,
                    "venue_id": 1,
                }
            },
            201,
            "create_event",
            {},
        ),
        ("GET", f"{api_prefix}/events/3", {}, 200, "event3", {}),
        (
            "PUT",
            f"{api_prefix}/events/1",
            {
                "json": {
                    "name": "An Updated Event",
                    "description": "An Updated Event Description",
                    "starts_at": "2025-01-01T00:00:00Z",
                    "duration": 120,
                }
            },
            200,
            "update_event_1",
            {},
        ),
        (
            "GET",
            f"{api_prefix}/venues/2/events",
            {},
            200,
            "events_venue_2",
            {},
        ),
        (
            "GET",
            f"{api_prefix}/events/in-range",
            {
                "params": {
                    "latitude": 48.1351,
                    "longitude": 11.5820,
                    "distance": 50,
                }
            },
            200,
            "events_50km_from_munich",
            {},
        ),
    ],
)
async def test_events(
    method,
    url,
    request_kwargs,
    response_code,
    response_data,
    response_diff_kwargs,
):
    fixture_data = await load_db_fixture("tests/fixtures/events.json")

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.request(method=method, url=url, **request_kwargs)

    assert response.status_code == response_code

    result = response.json()
    if result and isinstance(result, list):
        for item in result:
            item.pop("created_at", None)
            item.pop("updated_at", None)
            item.pop("venue", None)
            item.pop("distance_km", None)  # for /events/in-range
    elif result and isinstance(result, dict):
        result.pop("created_at", None)
        result.pop("updated_at", None)
        result.pop("venue", None)

    assert not DeepDiff(
        result,
        fixture_data["api_response"][response_data],
        ignore_order=True,
        **response_diff_kwargs,
    )
