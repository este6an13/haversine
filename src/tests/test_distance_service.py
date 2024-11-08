import pytest
from math import isclose
from src.services.distance_service.utils import haversine, calculate_distance
from src.database.models import Location


@pytest.mark.parametrize(
    "lat1, lon1, lat2, lon2, expected_distance",
    [
        (0, 0, 0, 0, 0),  # Same point
        (51.5074, -0.1278, 48.8566, 2.3522, 343.57),  # London to Paris
        (0, 0, 0, 90, 10007.54),  # Equator point at 0° and 90° longitude
    ],
)
def test_haversine(lat1, lon1, lat2, lon2, expected_distance):
    """Test haversine with various scenarios."""
    distance = haversine(lat1, lon1, lat2, lon2)
    assert isclose(distance, expected_distance, rel_tol=1e-2)


@pytest.mark.parametrize(
    "locations, expected_distance",
    [
        ([], 0),  # No points
        ([(51.5074, -0.1278)], 0),  # Single point (London)
        (
            [(51.5074, -0.1278), (48.8566, 2.3522), (40.7128, -74.0060)],
            6181.19,
        ),  # London -> Paris -> New York
    ],
)
def test_calculate_distance(locations, expected_distance):
    """Test calculate_distance with various input sets."""
    distance = calculate_distance(locations)
    assert isclose(distance, expected_distance, rel_tol=1e-2)
