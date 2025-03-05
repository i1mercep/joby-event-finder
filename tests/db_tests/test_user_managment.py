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
        (
            "GET",
            f"{api_prefix}/users",
            {},
            200,
            "users",
            {},
        ),
        (
            "GET",
            f"{api_prefix}/users/1",
            {},
            200,
            "user_1",
            {"exclude_paths": ["root['created_at']", "root['updated_at']"]},
        ),
        (
            "DELETE",
            f"{api_prefix}/users/3",
            {},
            200,
            "delete_user_b",
            {"exclude_paths": ["root['created_at']", "root['updated_at']"]},
        ),
        (
            "POST",
            f"{api_prefix}/users",
            {"json": {"username": "abrandnewuser", "email": "abrandnewuser@example.com"}},
            201,
            "create_abrandnewuser",
            {"exclude_paths": ["root['created_at']", "root['updated_at']"]},
        ),
        (
            "PUT",
            f"{api_prefix}/users/3",
            {
                "json": {
                    "username": "user_b_updated",
                }
            },
            200,
            "update_user_b",
            {"exclude_paths": ["root['created_at']", "root['updated_at']"]},
        ),
    ],
)
async def test_account_management(
    method,
    url,
    request_kwargs,
    response_code,
    response_data,
    response_diff_kwargs,
):
    fixture_data = await load_db_fixture("tests/fixtures/users.json")

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.request(method=method, url=url, **request_kwargs)

    assert response.status_code == response_code

    result = response.json()
    if result and isinstance(result, list):
        for item in result:
            item.pop("created_at", None)
            item.pop("updated_at", None)

    assert not DeepDiff(
        result,
        fixture_data["api_response"][response_data],
        ignore_order=True,
        **response_diff_kwargs,
    )
