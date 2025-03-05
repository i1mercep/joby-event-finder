import asyncio
import logging

from fastapi import HTTPException

from src.config import get_settings
from src.crud.app_user import crud_app_user
from src.db import SessionLocal
from src.models.app_user import AppUserCreate

_logger = logging.getLogger(__name__)


async def init_admin():
    settings = get_settings()
    if not settings.admin_username or not settings.admin_email:
        _logger.error("ADMIN_USERNAME or ADMIN_EMAIL not set!")
        return

    db = SessionLocal()
    try:
        user = AppUserCreate(username=settings.admin_username, email=settings.admin_email)
        try:
            user_db = await crud_app_user.create(db, user)
            _logger.info("Created admin user '%s' with id '%s'", user_db.username, user_db.id)
        except HTTPException:
            _logger.info("Admin user already exists")
    finally:
        await db.close()


async def main():
    await init_admin()


if __name__ == "__main__":
    asyncio.run(main())
