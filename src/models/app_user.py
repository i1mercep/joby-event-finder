from datetime import UTC, datetime
from typing import TYPE_CHECKING

from pydantic import field_validator
from sqlmodel import Column, DateTime, Field, Relationship, func

from src.models.base import Base
from src.validators import validate_email, validate_username

if TYPE_CHECKING:
    from src.models.venue import Venue


class AppUserBase(Base):
    username: str = Field(unique=True, index=True)
    email: str = Field(unique=True, index=True)

    @field_validator("username")
    @classmethod
    def validate_username(cls, v: str) -> str:
        return validate_username(v)

    @field_validator("email")
    @classmethod
    def validate_email(cls, v: str) -> str:
        return validate_email(v)


class AppUser(AppUserBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    disabled_at: datetime | None = None
    created_at: datetime = Field(sa_column=Column(DateTime(timezone=True), server_default=func.now(), nullable=False))
    updated_at: datetime = Field(
        sa_column=Column(
            DateTime(timezone=True), server_default=func.now(), onupdate=datetime.now(UTC), nullable=False
        ),
    )

    created_venues: list["Venue"] = Relationship(back_populates="created_by")


# AppUser Schemas
class AppUserCreate(AppUserBase):
    pass


class AppUserUpdate(Base):
    username: str | None = None
    email: str | None = None
    disable: bool | None = None

    @field_validator("username")
    @classmethod
    def validate_username(cls, v: str) -> str:
        return validate_username(v)

    @field_validator("email")
    @classmethod
    def validate_email(cls, v: str) -> str:
        return validate_email(v)
