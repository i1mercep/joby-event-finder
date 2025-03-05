from typing import Any

import pytest_asyncio

from src.db import SessionLocal, engine
from src.models.app_user import AppUser
from src.models.base import Base
from src.models.event import Event
from src.models.venue import Venue
from tests.conftest import load_fixture


@pytest_asyncio.fixture(autouse=True, loop_scope="session")
async def create_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


async def load_db_fixture(file_name: str) -> dict[str, Any]:
    data = load_fixture(file_name)

    if data:
        db = SessionLocal()
        try:
            async with db.begin():
                for user in data["db"].get("users", []):
                    db_user = AppUser(**user)
                    db.add(db_user)
                for venue in data["db"].get("venues", []):
                    db_venue = Venue(**venue)
                    db.add(db_venue)
                for event in data["db"].get("events", []):
                    db_event = Event(**event)
                    db.add(db_event)
        finally:
            await db.close()
    return data
