"""
City related functionality
"""
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship

from src.models.db.country import Country
from .base_model import BaseModel


class City(BaseModel):
    """City representation"""
    __tablename__ = "city"

    name = Column(String(120), nullable=False, unique=True)
    country_code = Column(String(3), ForeignKey(Country.country_code), nullable=False)

    country = relationship('Country', foreign_keys='City.country_code')

    def __repr__(self) -> str:
        """Dummy repr"""
        return f"<City {self.id} ({self.name})>"

    def to_dict(self) -> dict:
        """Dictionary representation of the object"""
        return {
            "id": self.id,
            "name": self.name,
            "country_code": self.country_code,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }

    @staticmethod
    def create(data: dict) -> "City":
        """Create a new city"""
        from src.persistence import repo

        country = Country.get(data["country_code"])

        if not country:
            raise ValueError("Country not found")

        city = City(**data)
        city.generate_id()

        repo.save(city)

        return city

    @staticmethod
    def update(city_id: str, data: dict) -> "City":
        """Update an existing city"""
        from src.persistence import repo

        city = City.get(city_id)

        if not city:
            raise ValueError("City not found")

        for key, value in data.items():
            setattr(city, key, value)

        repo.update(city)

        return city