from fastapi import FastAPI, BackgroundTasks
from pydantic import BaseModel
from src.services.distance_service.pubsub import request_queue, response_queue
from src.database.repositories.location_repository import LocationRepository
from src.database.db import get_session
from src.services.distance_service.utils import calculate_distance
from src.logger import get_logger
import threading


app = FastAPI(
    title="Distance API",
    version="1.0",
    description="Calculate distances between locations",
)

logger = get_logger()


# Request model for validation and Swagger docs
class DistanceRequest(BaseModel):
    ids: list[int]


# Response model for Swagger docs
class DistanceResponse(BaseModel):
    distance: float


# Background worker function to process location IDs and compute distances
def worker():
    """Background worker that processes location IDs and computes distances."""
    while True:
        location_ids = request_queue.get()
        if location_ids is None:
            logger.info("Worker received stop signal.")
            break

        logger.info("Worker processing location IDs", location_ids=location_ids)

        try:
            session = get_session()
            repository = LocationRepository(session)
            locations = repository.get_locations_by_ids(location_ids)
            session.close()

            # Handle if no locations are found
            if not locations:
                logger.error(
                    "No locations found for the given IDs", location_ids=location_ids
                )
                continue

            lat_lon_pairs = [(loc.latitude, loc.longitude) for loc in locations]
            distance = calculate_distance(lat_lon_pairs)
            logger.info("Distance calculated", distance=distance)

            response_queue.put({"distance": distance})

        except Exception as e:
            logger.error("Error in worker processing", error=str(e))


# Endpoint for calculating distance
@app.post("/distance/", response_model=DistanceResponse)
async def calculate_distance_endpoint(
    distance_request: DistanceRequest, background_tasks: BackgroundTasks
):
    """Calculate distance between a list of location IDs."""
    location_ids = distance_request.ids
    logger.info("Received distance request", location_ids=location_ids)

    request_queue.put(location_ids)

    # This will ensure that the worker function runs in the background
    background_tasks.add_task(worker)

    # Get the result from the response queue
    # (This is a blocking operation, ideally, you'd want to use async mechanisms)
    result = response_queue.get()

    logger.info("Distance result sent to client", result=result)
    return result


if __name__ == "__main__":
    import uvicorn

    # Start the background worker in a separate thread
    threading.Thread(target=worker, daemon=True).start()
    uvicorn.run(app, host="0.0.0.0", port=5001)
