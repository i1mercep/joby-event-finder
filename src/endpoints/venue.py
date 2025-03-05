from fastapi import APIRouter, status

from src.crud.distance import haversine_distance
from src.crud.event import crud_event
from src.crud.venue import crud_venue
from src.db import SessionDep
from src.models.event import EventRead
from src.models.venue import VenueCreate, VenueRead, VenueReadWithDistance, VenueUpdate
from src.params import Latitude, Limit, Longitude, Offset, RangeKm

router = APIRouter(prefix="/venues")


@router.post("", status_code=status.HTTP_201_CREATED, summary="Create a venue")
async def create(venue: VenueCreate, db: SessionDep) -> VenueRead:
    return await crud_venue.create(db, venue)


@router.get("", summary="Get all venues")
async def get_multi(db: SessionDep, offset: int = 0, limit: int = 100) -> list[VenueRead]:
    return await crud_venue.get_multi(db, offset, limit)


# ruff: noqa: PLR0913, PLR0917
@router.get("/in-range", summary="Get venues in range")
async def get_in_range(
    db: SessionDep,
    latitude: Latitude,
    longitude: Longitude,
    range_km: RangeKm = 20,
    offset: Offset = 0,
    limit: Limit = 100,
) -> list[VenueReadWithDistance]:
    """Get all venues in range from coordinates."""
    venues = await crud_venue.get_venues_in_range(db, latitude, longitude, range_km, offset, limit)
    venues_with_distance = []
    for venue in venues:
        distance = haversine_distance(latitude, longitude, venue.latitude, venue.longitude)
        venues_with_distance.append(VenueReadWithDistance(**venue.model_dump(), distance_km=distance))
    return venues_with_distance


@router.get("/{venue_id}", summary="Get a venue by ID")
async def get(venue_id: int, db: SessionDep) -> VenueRead:
    return await crud_venue.get(db, venue_id)


@router.get("/{venue_id}/events", summary="Get events at a venue")
async def get_venue_events(venue_id: int, db: SessionDep) -> list[EventRead]:
    return await crud_event.get_events_at_venue(db, venue_id)


@router.put("/{venue_id}", summary="Update a venue by ID")
async def update(venue_id: int, venue: VenueUpdate, db: SessionDep) -> VenueRead:
    return await crud_venue.update(db, venue_id, venue)


@router.delete("/{venue_id}", summary="Delete a venue by ID")
async def delete(venue_id: int, db: SessionDep) -> VenueRead:
    return await crud_venue.delete(db, venue_id)
