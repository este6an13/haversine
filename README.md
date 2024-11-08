# Haversine: A Microservices Haversine Distance Calculator

A microservices-based solution for a planning company's delivery route distance calculation problem. The system consists of two REST API microservices:

1. Location Service: Registers locations (name, latitude, longitude) and returns unique IDs
2. Distance Service: Calculates the total distance of a delivery route using the Haversine formula, processing location IDs through a pub/sub queue

## Design

The project follows a microservices architecture with the following general structure:

```bash
src/
├── database/
│   └── db.py
│   └── models.py
│   └── repositories/
│       └── location_repository.py
├── services/
│   ├── location_service/
│   │   └── app.py
│   └── distance_service/
│       └── app.py
│       └── pubsub.py
│       └── utils.py
└── tests/
    ├── conftest.py
    ├── test_location_service.py
    └── test_distance_service.py
```

- The Location Service handles location registration and storage using SQLite through the LocationRepository class
- The Distance Service implements a background worker thread with a queue system for processing distance calculations
- Both services are built using FastAPI
- Both services use the Location Repository to interact with the database

## Running the Application

### Without Docker

1. Install dependencies using Poetry:

    ```bash
    poetry install
    ```

2. Start the Location Service (runs on port 5000):

    ```bash
    poetry run python src/services/location_service/app.py
    ```

3. In a new terminal, start the Distance Service (runs on port 5001):

    ```bash
    poetry run python src/services/distance_service/app.py
    ```

### Build With Docker

1. Build and start both services:

    ```bash
    docker-compose build
    docker-compose up
    ```

The services will be available at:

- Location Service: `http://localhost:5000`
- Distance Service: `http://localhost:5001`

## Running Tests

### Run Tests Without Docker

Run tests for each service:

```bash
poetry run pytest src/tests/test_location_service.py
poetry run pytest src/tests/test_distance_service.py
```

### Run Tests With Docker

Run tests for each service in the Docker environment:

```bash
docker-compose run location-service poetry run pytest src/tests/test_location_service.py
docker-compose run distance-service poetry run pytest src/tests/test_distance_service.py
```

## API Documentation

Once the services are running, you can access the API documentation at:

- Location Service: `http://localhost:5000/docs`
- Distance Service: `http://localhost:5001/docs`
