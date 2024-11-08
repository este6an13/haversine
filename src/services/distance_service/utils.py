import math


def haversine(lat1, lon1, lat2, lon2):
    """Calculate the great-circle distance between two points on Earth."""
    R = 6371  # Earth radius in km
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)
    a = (
        math.sin(delta_phi / 2) ** 2
        + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2) ** 2
    )
    return 2 * R * math.atan2(math.sqrt(a), math.sqrt(1 - a))


def calculate_distance(locations):
    """Calculate the total distance for a series of latitude/longitude pairs."""
    distance = 0.0
    for i in range(len(locations) - 1):
        lat1, lon1 = locations[i]
        lat2, lon2 = locations[i + 1]
        distance += haversine(lat1, lon1, lat2, lon2)
    return distance
