from fastapi import APIRouter, status

from src.crud.distance import haversine_distance
from src.crud.event import crud_event
from src.db import SessionDep
from src.models.event import EventCreate, EventReadWithDistance, EventReadWithVenue, EventUpdate
from src.params import Latitude, Limit, Longitude, Offset, RangeKm

router = APIRouter(prefix="/events")


@router.post("", status_code=status.HTTP_201_CREATED, summary="Create an event")
async def create(event: EventCreate, db: SessionDep) -> EventReadWithVenue:
    """Create a new event"""
    return await crud_event.create(db, event)


@router.get("", summary="Get events")
async def get_multi(db: SessionDep, offset: Offset = 0, limit: Limit = 100) -> list[EventReadWithVenue]:
    """Get all active events."""
    return await crud_event.get_multi(db, offset, limit)


# ruff: noqa: PLR0913, PLR0917
@router.get("/in-range", summary="Get events in range")
async def get_events_in_range(
    db: SessionDep,
    latitude: Latitude,
    longitude: Longitude,
    range_km: RangeKm = 20,
    offset: Offset = 0,
    limit: Limit = 100,
) -> list[EventReadWithDistance]:
    """Get all events in range from coordinates."""
    events = await crud_event.get_events_in_range(db, latitude, longitude, range_km, offset, limit)
    events_with_distance = []
    for event in events:
        distance = haversine_distance(latitude, longitude, event.venue.latitude, event.venue.longitude)
        events_with_distance.append(
            EventReadWithDistance(**event.model_dump(), venue=event.venue, distance_km=distance)
        )
    return events_with_distance


@router.get("/{event_id}", summary="Get event by ID")
async def get(event_id: int, db: SessionDep) -> EventReadWithVenue:
    """Get a specific event."""
    return await crud_event.get(db, event_id)


@router.put("/{event_id}", summary="Update event by ID")
async def update(event_id: int, event: EventUpdate, db: SessionDep) -> EventReadWithVenue:
    """Update a specific event."""
    return await crud_event.update(db, event_id, event)


@router.delete("/{event_id}", summary="Delete event by ID")
async def delete(event_id: int, db: SessionDep) -> EventReadWithVenue:
    """Delete a specific event."""
    return await crud_event.delete(db, event_id)
