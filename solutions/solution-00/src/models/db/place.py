"""
Place related functionality
"""
from sqlalchemy import Column, String, Float, ForeignKey, Integer
from sqlalchemy.orm import relationship

from src.models.db.city import City
from src.models.db.user import User
from .base_model import BaseModel


class Place(BaseModel):
    """Place representation"""
    __tablename__ = "place"

    name = Column(String(120), nullable=False, unique=True)
    description = Column(String, nullable=False)
    address = Column(String, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    host_id = Column(String(256), ForeignKey(User.id), nullable=False)
    city_id = Column(String(256), ForeignKey(City.id), nullable=False)
    price_per_night = Column(Integer, nullable=False)
    number_of_rooms = Column(Integer, nullable=False)
    number_of_bathrooms = Column(Integer, nullable=False)
    max_guests = Column(Integer, nullable=False)

    amenities = relationship("PlaceAmenity", back_populates="place")

    def __repr__(self) -> str:
        """Dummy repr"""
        return f"<Place {self.id} ({self.name})>"

    def to_dict(self) -> dict:
        """Dictionary representation of the object"""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "address": self.address,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "city_id": self.city_id,
            "host_id": self.host_id,
            "price_per_night": self.price_per_night,
            "number_of_rooms": self.number_of_rooms,
            "number_of_bathrooms": self.number_of_bathrooms,
            "max_guests": self.max_guests,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }

    @staticmethod
    def create(data: dict) -> "Place":
        """Create a new place"""
        from src.persistence import repo

        user: User | None = User.get(data["host_id"])

        if not user:
            raise ValueError(f"User with ID {data['host_id']} not found")

        city: City | None = City.get(data["city_id"])

        if not city:
            raise ValueError(f"City with ID {data['city_id']} not found")

        new_place = Place(**data)
        new_place.generate_id()

        repo.save(new_place)

        return new_place

    @staticmethod
    def update(place_id: str, data: dict) -> "Place | None":
        """Update an existing place"""
        from src.persistence import repo

        place: Place | None = Place.get(place_id)

        if not place:
            return None

        for key, value in data.items():
            setattr(place, key, value)

        repo.update(place)

        return place