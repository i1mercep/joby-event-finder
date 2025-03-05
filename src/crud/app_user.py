from datetime import UTC, datetime

from fastapi import HTTPException, status
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.crud.base import CRUDBase
from src.models.app_user import AppUser, AppUserCreate, AppUserUpdate


class CRUDAppUser(CRUDBase[AppUser, AppUserCreate, AppUserUpdate]):
    async def get_by_username(self, db: AsyncSession, username: str) -> AppUser:
        result = await db.exec(select(AppUser).where(AppUser.username == username))
        return result.first()

    async def get_by_email(self, db: AsyncSession, email: str) -> AppUser:
        result = await db.exec(select(AppUser).where(AppUser.email == email))
        return result.first()

    async def get_multi(self, db: AsyncSession, offset: int = 0, limit: int = 100) -> list[AppUser]:
        """Get active users."""
        stmt = select(AppUser).offset(offset).limit(limit)
        result = await db.exec(stmt)
        return result.all()

    async def create(self, db: AsyncSession, user: AppUserCreate) -> AppUser:
        """Create one new user."""
        db_user = await crud_app_user.get_by_username(db, user.username)
        if db_user:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already exists")
        db_user = await crud_app_user.get_by_email(db, user.email)
        if db_user:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already exists")
        return await super().create(db, user)

    async def update(self, db: AsyncSession, user_id: int, user: AppUserUpdate) -> AppUser:
        """Update specific user."""
        disable = user.disable
        user.disable = None
        db_user = await super().update(db, user_id, user)
        if disable:
            db_user.disabled_at = datetime.now(UTC)
            db.add(db_user)
            await db.commit()
            await db.refresh(db_user)
        return db_user


crud_app_user = CRUDAppUser(AppUser)
