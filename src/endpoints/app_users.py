from fastapi import APIRouter, status

from src.crud.app_user import crud_app_user
from src.db import SessionDep
from src.models.app_user import AppUser, AppUserCreate, AppUserUpdate
from src.params import Limit, Offset

router = APIRouter(prefix="/users")


@router.get("/{user_id}", summary="Get a user by ID")
async def get_user(db: SessionDep, user_id: int) -> AppUser:
    return await crud_app_user.get(db, user_id)


@router.get("", summary="Get all users")
async def get_users(db: SessionDep, offset: Offset = 0, limit: Limit = 100) -> list[AppUser]:
    return await crud_app_user.get_multi(db, offset, limit)


@router.post("", status_code=status.HTTP_201_CREATED, summary="Create a user")
async def create_user(db: SessionDep, user: AppUserCreate) -> AppUser:
    return await crud_app_user.create(db, user)


@router.put("/{user_id}", summary="Update a user by ID")
async def update_user(db: SessionDep, user_id: int, user: AppUserUpdate) -> AppUser:
    return await crud_app_user.update(db, user_id, user)


@router.delete("/{user_id}", summary="Delete a user by ID")
async def delete_user(db: SessionDep, user_id: int) -> AppUser:
    return await crud_app_user.delete(db, user_id)
