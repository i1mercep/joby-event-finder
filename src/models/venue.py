from datetime import UTC, datetime
from typing import TYPE_CHECKING

from pydantic import field_validator
from sqlmodel import Column, DateTime, Field, Relationship, func

from src.models.base import Base, Distance
from src.validators import convert_naive_to_utc

if TYPE_CHECKING:
    from src.models.app_user import AppUser
    from src.models.event import Event


class Venue(Base, table=True):
    """A venue where events take place."""

    id: int = Field(primary_key=True)
    name: str
    description: str | None = None
    longitude: float
    latitude: float
    created_at: datetime = Field(sa_column=Column(DateTime(timezone=True), server_default=func.now(), nullable=False))
    updated_at: datetime = Field(
        sa_column=Column(
            DateTime(timezone=True), server_default=func.now(), onupdate=datetime.now(UTC), nullable=False
        ),
    )
    user_id: int = Field(foreign_key="app_user.id")

    events: list["Event"] = Relationship(back_populates="venue", cascade_delete=True)
    created_by: "AppUser" = Relationship(back_populates="created_venues")

    @field_validator("updated_at", "created_at")
    @staticmethod
    def validate_ts(v: datetime) -> datetime:
        return convert_naive_to_utc(v)


class VenueRead(Base):
    id: int
    name: str
    description: str | None = None
    longitude: float
    latitude: float
    user_id: int


class VenueReadWithDistance(VenueRead, Distance):
    pass


class VenueCreate(Base):
    name: str
    description: str | None = None
    longitude: float
    latitude: float
    user_id: int


class VenueUpdate(Base):
    name: str | None = None
    description: str | None = None
    longitude: float | None = None
    latitude: float | None = None
