import pytest

from src.crud.distance import BoundingBox, get_bounding_box, haversine_distance


@pytest.mark.parametrize(
    "latitude, longitude, range_km, expected_bbox",
    [
        (52.52, 13.405, 10, BoundingBox(52.42, 52.62, 13.305, 13.505)),
        (0, 0, 0, BoundingBox(0, 0, 0, 0)),
        (34.0522, -118.2437, 50, BoundingBox(33.5522, 34.5522, -118.7437, -117.7437)),  # Los Angeles with 50km range
        (-33.8688, 151.2093, 20, BoundingBox(-34.0688, -33.6688, 151.0093, 151.4093)),  # Sydney with 20km range
    ],
    ids=["Berlin 10km", "Zero", "LA 50km", "Sydney 20km"],
)
def test_get_bounding_box(latitude, longitude, range_km, expected_bbox):
    bbox = get_bounding_box(latitude, longitude, range_km)
    assert isinstance(bbox, BoundingBox)
    assert bbox.lat_min == pytest.approx(expected_bbox.lat_min, rel=1e-2)
    assert bbox.lat_max == pytest.approx(expected_bbox.lat_max, rel=1e-2)
    assert bbox.lon_min == pytest.approx(expected_bbox.lon_min, rel=1e-2)
    assert bbox.lon_max == pytest.approx(expected_bbox.lon_max, rel=1e-2)


@pytest.mark.parametrize(
    "lat1, lon1, lat2, lon2, expected_distance",
    [
        (52.52, 13.405, 48.8566, 2.3522, 878.84),
        (52.52, 13.405, 52.52, 13.405, 0),
        (34.0522, -118.2437, 40.7128, -74.0060, 3940.07),
        (-33.8688, 151.2093, 35.6895, 139.6917, 7826.62),
    ],
    ids=["Berlin to Paris", "Same point", "LA to NYC", "Sydney to Tokyo"],
)
def test_haversine_distance(lat1, lon1, lat2, lon2, expected_distance):
    distance = haversine_distance(lat1, lon1, lat2, lon2)
    assert isinstance(distance, float)
    assert distance >= 0
    assert distance == pytest.approx(expected_distance, rel=1e-2)
