from src.database.models import Location


class LocationRepository:
    def __init__(self, session):
        self.session = session

    def add_location(self, name, latitude, longitude):
        location = Location(name=name, latitude=latitude, longitude=longitude)
        self.session.add(location)
        self.session.commit()
        self.session.refresh(location)
        return location.id

    def get_locations_by_ids(self, ids):
        return self.session.query(Location).filter(Location.id.in_(ids)).all()
