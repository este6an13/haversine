import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from src.database.db import get_session
from src.database.models import Base
from src.database.repositories.location_repository import LocationRepository
from src.services.location_service.app import app as location_app

# Database URL with in-memory SQLite and multi-threading enabled
TEST_DATABASE_URL = "sqlite:///:memory:"

# Setup the test database engine
test_engine = create_engine(
    TEST_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Create a sessionmaker without directly binding to the engine
SessionLocal = sessionmaker(autocommit=False, autoflush=False)


@pytest.fixture(scope="session", autouse=True)
def setup_test_database():
    """Sets up and tears down the test database."""
    # Create tables for the entire session once
    Base.metadata.create_all(bind=test_engine)
    yield
    # Drop tables after tests complete
    Base.metadata.drop_all(bind=test_engine)


@pytest.fixture
def session():
    """Creates a new transactional session for a test."""
    connection = test_engine.connect()
    transaction = connection.begin()

    # Bind sessionmaker to the current connection for each test
    TestSession = scoped_session(SessionLocal)
    session = TestSession(bind=connection)

    yield session

    # Cleanup after test
    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture
def client():
    return TestClient(location_app)


@pytest.fixture
def vehicle_repository(session):
    return LocationRepository(session)
