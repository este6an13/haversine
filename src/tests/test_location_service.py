import pytest
from fastapi.testclient import TestClient

from src.database.models import Location


@pytest.mark.parametrize(
    "payload, expected_status",
    [
        # Test case 1: Valid location data
        (
            {
                "name": "Test Location 1",
                "latitude": 40.7128,
                "longitude": -74.0060,
            },
            201,
        ),
        # Test case 2: Invalid data (missing latitude)
        (
            {
                "name": "Test Location 2",
                "longitude": -74.0060,
            },
            422,
        ),
        # Test case 3: Invalid data (latitude out of range)
        (
            {
                "name": "Test Location 3",
                "latitude": 100.0,  # Invalid latitude
                "longitude": -74.0060,
            },
            422,
        ),
    ],
)
def test_add_location_endpoint(client: TestClient, session, payload, expected_status):
    """Test the /locations/ endpoint for adding new locations."""

    # Send a POST request with the test payload
    response = client.post("/locations/", json=payload)

    # Verify the response status code
    assert response.status_code == expected_status
