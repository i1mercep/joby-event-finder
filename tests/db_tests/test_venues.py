import os
import unittest

import pytest
from deepdiff import DeepDiff
from httpx import ASGITransport, AsyncClient

from src.config import get_settings
from src.main import app
from tests.conftest import load_db_fixture

DOCKER_CONTAINER = os.getenv("DOCKER_CONTAINER", "False").lower() == "true"
settings = get_settings()
api_prefix = settings.api_prefix


@unittest.skipUnless(DOCKER_CONTAINER, "Don't run this test locally")
@pytest.mark.asyncio(loop_scope="session")
@pytest.mark.parametrize(
    "method, url, request_kwargs, response_code, response_data, response_diff_kwargs",
    [
        ("GET", f"{api_prefix}/venues", {}, 200, "all_venues", {}),
        ("DELETE", f"{api_prefix}/venues/1", {}, 200, "delete_venue_1", {}),
        (
            "POST",
            f"{api_prefix}/venues",
            {
                "json": {
                    "name": "New name",
                    "description": "New description",
                    "latitude": 6.0,
                    "longitude": 9.0,
                    "user_id": 1,
                }
            },
            201,
            "create_venue",
            {},
        ),
        ("GET", f"{api_prefix}/venues/3", {}, 200, "venue3", {}),
        (
            "PUT",
            f"{api_prefix}/venues/1",
            {
                "json": {
                    "name": "Updated venue",
                    "description": "Updated description",
                    "latitude": 4.0,
                    "longitude": 20.0,
                }
            },
            200,
            "update_venue_1",
            {},
        ),
    ],
)
async def test_venues(
    method,
    url,
    request_kwargs,
    response_code,
    response_data,
    response_diff_kwargs,
):
    fixture_data = await load_db_fixture("tests/fixtures/venues.json")

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.request(method=method, url=url, **request_kwargs)

    assert response.status_code == response_code

    result = response.json()
    if result and isinstance(result, list):
        for item in result:
            item.pop("created_at", None)
            item.pop("updated_at", None)
    elif result and isinstance(result, dict):
        result.pop("created_at", None)
        result.pop("updated_at", None)

    assert not DeepDiff(
        result,
        fixture_data["api_response"][response_data],
        ignore_order=True,
        **response_diff_kwargs,
    )
