from datetime import UTC, datetime

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.crud.base import CRUDBase
from src.crud.distance import get_bounding_box
from src.models.event import Event, EventCreate, EventUpdate
from src.models.venue import Venue
from src.params import Limit, Offset


class CRUDEvent(CRUDBase[Event, EventCreate, EventUpdate]):
    async def get_multi(self, db: AsyncSession, offset: Offset = 0, limit: Limit = 100) -> list[Event]:
        """Get events."""
        stmt = select(Event).offset(offset).limit(limit)
        result = await db.exec(stmt)
        return result.all()

    async def get_events_in_range(
        self,
        db: AsyncSession,
        latitude: float,
        longitude: float,
        range_km: float,
        offset: Offset = 0,
        limit: Limit = 100,
    ) -> list[Event]:
        """Get all events in range from coordinates."""
        box = get_bounding_box(latitude, longitude, range_km)
        # Query only venues within range
        stmt = (
            select(Event)
            .join(Event.venue)
            .filter(
                Venue.latitude >= box.lat_min,
                Venue.latitude <= box.lat_max,
                Venue.longitude >= box.lon_min,
                Venue.longitude <= box.lon_max,
            )
            .offset(offset)
            .limit(limit)
        )

        result = await db.exec(stmt)
        return result.all()

    async def get_events_at_venue(
        self, db: AsyncSession, venue_id: int, offset: Offset = 0, limit: Limit = 100
    ) -> list[Event]:
        stmt = select(Event).where(Event.venue_id == venue_id).offset(offset).limit(limit)
        result = await db.exec(stmt)
        return result.all()

    async def cancel(self, db: AsyncSession, event_id: int) -> Event:
        """Cancel an event."""
        db_event = await self.get(db, event_id)
        db_event.cancelled_at = datetime.now(UTC)
        db.add(db_event)
        await db.commit()
        await db.refresh(db_event)
        return db_event

    async def update(self, db: AsyncSession, event_id: int, event_update: EventUpdate) -> Event:
        """Update specific event."""
        db_event = await self.get(db, event_id)
        if event_update.cancel:
            return await self.cancel(db, event_id)
        update_data = event_update.model_dump(exclude_unset=True, exclude={"cancel"})
        for field, value in update_data.items():
            setattr(db_event, field, value)
        db.add(db_event)
        await db.commit()
        await db.refresh(db_event)
        return db_event


crud_event = CRUDEvent(Event)
