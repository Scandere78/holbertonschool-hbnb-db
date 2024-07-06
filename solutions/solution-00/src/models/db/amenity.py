"""
Amenity related functionality
"""
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship

from src.models.db.place import Place
from .base_model import BaseModel


class Amenity(BaseModel):
    """Amenity representation"""
    __tablename__ = "amenity"

    name = Column(String(150), unique=True, nullable=False)

    def __repr__(self) -> str:
        """Dummy repr"""
        return f"<Amenity {self.id} ({self.name})>"

    def to_dict(self) -> dict:
        """Dictionary representation of the object"""
        return {
            "id": self.id,
            "name": self.name,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }

    @staticmethod
    def create(data: dict) -> "Amenity":
        """Create a new amenity"""
        from src.persistence import repo

        new_amenity = Amenity(**data)
        new_amenity.generate_id()

        repo.save(new_amenity)

        return new_amenity

    @staticmethod
    def update(amenity_id: str, data: dict) -> "Amenity | None":
        """Update an existing amenity"""
        from src.persistence import repo

        amenity: Amenity | None = Amenity.get(amenity_id)

        if not amenity:
            return None

        if "name" in data:
            amenity.name = data["name"]

        repo.update(amenity)

        return amenity


class PlaceAmenity(BaseModel):
    """PlaceAmenity representation"""
    __tablename__ = "placeamenity"

    name = Column(String(150), unique=True, nullable=False)
    place_id = Column(String(256), ForeignKey(Place.id), nullable=False)
    amenity_id = Column(String(256), ForeignKey(Amenity.id), nullable=False)

    place = relationship('Place', foreign_keys='PlaceAmenity.place_id')
    amenity = relationship('Amenity', foreign_keys='PlaceAmenity.amenity_id')

    def __repr__(self) -> str:
        """Dummy repr"""
        return f"<PlaceAmenity ({self.place.id} - {self.amenity.id})>"

    def to_dict(self) -> dict:
        """Dictionary representation of the object"""
        return {
            "id": self.id,
            "place_id": self.place.id,
            "amenity_id": self.amenity.id,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }

    @staticmethod
    def get(place_id: str, amenity_id: str) -> "PlaceAmenity | None":
        """Get a PlaceAmenity object by place_id and amenity_id"""
        from src.persistence import repo

        place_amenities: list[PlaceAmenity] = repo.get_all("placeamenity")

        for place_amenity in place_amenities:
            if (
                place_amenity.place_id == place_id
                and place_amenity.amenity_id == amenity_id
            ):
                return place_amenity

        return None

    @staticmethod
    def create(data: dict) -> "PlaceAmenity":
        """Create a new PlaceAmenity object"""
        from src.persistence import repo

        new_place_amenity = PlaceAmenity(**data)

        repo.save(new_place_amenity)

        return new_place_amenity

    @staticmethod
    def delete(place_id: str, amenity_id: str) -> bool:
        """Delete a PlaceAmenity object by place_id and amenity_id"""
        from src.persistence import repo

        place_amenity = PlaceAmenity.get(place_id, amenity_id)

        if not place_amenity:
            return False

        repo.delete(place_amenity)

        return True

    @staticmethod
    def update(entity_id: str, data: dict):
        """Not implemented, isn't needed"""
        raise NotImplementedError(
            "This method is defined only because of the Base class"
        )