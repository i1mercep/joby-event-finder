from datetime import UTC, datetime
from typing import TYPE_CHECKING

from pydantic import field_validator
from sqlmodel import Column, DateTime, Field, Relationship, func

from src.models.base import Base, Distance
from src.models.venue import VenueRead
from src.validators import convert_naive_to_utc, validate_non_naive

if TYPE_CHECKING:
    from src.models.venue import Venue


class Event(Base, table=True):
    """An event that takes place at a venue."""

    id: int = Field(primary_key=True)
    name: str
    description: str
    starts_at: datetime = Field(sa_column=Column(DateTime(timezone=True), nullable=False))
    cancelled_at: datetime | None = None
    duration: int = Field(gt=0, le=1440, description="Duration in minutes")
    created_at: datetime = Field(sa_column=Column(DateTime(timezone=True), server_default=func.now(), nullable=False))
    updated_at: datetime = Field(
        sa_column=Column(
            DateTime(timezone=True), server_default=func.now(), onupdate=datetime.now(UTC), nullable=False
        ),
    )
    venue_id: int = Field(foreign_key="venue.id", nullable=False)
    venue: "Venue" = Relationship(back_populates="events", sa_relationship_kwargs={"lazy": "joined"})

    @field_validator("starts_at", "updated_at", "created_at")
    @staticmethod
    def validate_ts(v: datetime) -> datetime:
        return convert_naive_to_utc(v)


class EventRead(Base):
    id: int
    name: str
    description: str
    starts_at: datetime
    cancelled_at: datetime | None = None
    duration: int

    @field_validator("starts_at")
    @staticmethod
    def validate_ts(v: datetime) -> datetime:
        return convert_naive_to_utc(v)


class EventReadWithVenue(EventRead):
    venue: "VenueRead"


class EventReadWithDistance(EventReadWithVenue, Distance):
    pass


class EventCreate(Base):
    name: str
    description: str
    starts_at: datetime
    duration: int
    venue_id: int

    @field_validator("starts_at")
    @staticmethod
    def validate_starts_at(v: datetime) -> datetime:
        return validate_non_naive(v).replace(microsecond=0).astimezone(UTC)


class EventUpdate(Base):
    name: str | None = None
    description: str | None = None
    starts_at: datetime | None = None
    duration: int | None = None
    venue_id: int | None = None
    cancel: bool | None = None
