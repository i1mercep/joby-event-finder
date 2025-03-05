from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.crud.base import CRUDBase
from src.crud.distance import get_bounding_box
from src.models.venue import Venue, VenueCreate, VenueUpdate
from src.params import Limit, Offset


class CRUDVenue(CRUDBase[Venue, VenueCreate, VenueUpdate]):
    async def get_venues_in_range(
        self,
        db: AsyncSession,
        latitude: float,
        longitude: float,
        range_km: float,
        offset: Offset = 0,
        limit: Limit = 100,
    ) -> list[Venue]:
        """Get all venues in range from coordinates."""
        box = get_bounding_box(latitude, longitude, range_km)
        stmt = (
            select(Venue)
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


crud_venue = CRUDVenue(Venue)
