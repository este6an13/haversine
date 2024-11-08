from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel, Field, ValidationError
from sqlalchemy.orm import Session
from src.database.repositories.location_repository import LocationRepository
from src.database.db import get_session, init_db
from src.logger import get_logger


app = FastAPI(
    title="Location API",
    version="1.0",
    description="Manage locations",
)


logger = get_logger()


# Define Pydantic model for request validation
class Location(BaseModel):
    name: str = Field(..., description="The name of the location")
    latitude: float = Field(
        ..., ge=-90, le=90, description="Latitude of the location (-90 to 90)"
    )
    longitude: float = Field(
        ..., ge=-180, le=180, description="Longitude of the location (-180 to 180)"
    )


@app.post("/locations/", status_code=201, response_model=dict)
def add_location(location: Location, db: Session = Depends(get_session)):
    """
    Add a new location.
    """
    logger.info(
        "Adding new location",
        location_name=location.name,
        latitude=location.latitude,
        longitude=location.longitude,
    )

    try:
        repository = LocationRepository(db)
        location_id = repository.add_location(
            location.name, location.latitude, location.longitude
        )
        logger.info("Location added successfully", location_id=location_id)
        return {"id": location_id}
    except ValidationError as e:
        logger.error("Validation error", error=str(e), location_name=location.name)
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error("Unexpected error", error=str(e), location_name=location.name)
        raise HTTPException(status_code=500, detail="Internal Server Error")


if __name__ == "__main__":
    import uvicorn

    init_db()
    uvicorn.run(app, host="0.0.0.0", port=5000)
