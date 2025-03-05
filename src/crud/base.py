"""CRUD Base module."""

from typing import TypeVar

from fastapi import HTTPException, status
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.models.base import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=Base)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=Base)


class CRUDBase[ModelType, CreateSchemaType, UpdateSchemaType]:
    """CRUD object with default methods to Create, Read, Update, Delete (CRUD)."""

    def __init__(self, model: type[ModelType]):
        """CRUD Base constructor"""
        self.model = model

    async def get(self, db: AsyncSession, item_id: int) -> ModelType:
        """Get one by id."""
        item = await db.get(self.model, item_id)
        if item is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
        return item

    async def get_multi(self, db: AsyncSession, offset: int = 0, limit: int = 100) -> list[ModelType]:
        """Get multiple entries with pagination."""
        result = await db.exec(select(self.model).offset(offset).limit(limit))
        return result.all()

    async def create(self, db: AsyncSession, create_item: CreateSchemaType) -> ModelType:
        """Create one new entry."""
        db_obj = self.model(**create_item.model_dump())
        if not db.in_transaction():
            async with db.begin():
                db.add(db_obj)
        else:
            db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def update(self, db: AsyncSession, item_id: int, update_item: UpdateSchemaType) -> ModelType:
        """Update specific model."""
        db_obj = await self.get(db, item_id)
        update_data = update_item.model_dump(exclude_unset=True, exclude_none=True)
        for field, value in update_data.items():
            setattr(db_obj, field, value)

        if not db.in_transaction():
            async with db.begin():
                db.add(db_obj)
        else:
            db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def delete(self, db: AsyncSession, item_id: int) -> ModelType:
        """Remove model by id."""
        db_obj = await self.get(db, item_id)
        if not db.in_transaction():
            async with db.begin():
                await db.delete(db_obj)
        else:
            await db.delete(db_obj)
        await db.commit()
        return db_obj
