from math import asin, cos, pi, radians, sin, sqrt
from typing import NamedTuple

EARTH_RADIUS_KM = 6371.0


class BoundingBox(NamedTuple):
    lat_min: float
    lat_max: float
    lon_min: float
    lon_max: float


def get_bounding_box(latitude: float, longitude: float, range_km: float) -> BoundingBox:
    """Calculate the bounding box coordinates to filter venues within range."""
    delta_deg = (range_km / EARTH_RADIUS_KM) * (180 / pi)
    lat_min = latitude - delta_deg
    lat_max = latitude + delta_deg
    lon_min = longitude - delta_deg / cos(radians(latitude))
    lon_max = longitude + delta_deg / cos(radians(latitude))
    return BoundingBox(lat_min, lat_max, lon_min, lon_max)


def haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Calculate the haversine distance between two coordinates."""
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat / 2) ** 2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2) ** 2
    return 2 * EARTH_RADIUS_KM * asin(sqrt(a))
