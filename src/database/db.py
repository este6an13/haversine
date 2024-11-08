from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from src.database.models import Base

DATABASE_URL = "sqlite:///src/database/haversine.db"

# Set up SQLAlchemy engine and session
engine = create_engine(DATABASE_URL, echo=True)
Session = scoped_session(sessionmaker(bind=engine))


def get_session():
    engine = create_engine(DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db_session = SessionLocal()
    return db_session


def init_db():
    Base.metadata.create_all(bind=engine)
