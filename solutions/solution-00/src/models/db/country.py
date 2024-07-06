"""
Coutry related functionality
"""
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from .base_model import BaseModel


class Country(BaseModel):
    """Country representation"""
    __tablename__ = "country"

    name = Column(String(120), nullable=False, unique=True)
    country_code = Column(String(3), nullable=False, unique=True)

    cities = relationship("City", back_populates="country")

    def __repr__(self) -> str:
        """Dummy repr"""
        return f"<Country {self.country_code} ({self.name})>"

    def to_dict(self) -> dict:
        """Returns the dictionary representation of the country"""
        return {
            "name": self.name,
            "country_code": self.country_code,
        }
    
    @staticmethod
    def get_all() -> list["Country"]:
        """Get all countries"""
        from src.persistence import repo

        countries: list["Country"] = repo.get_all(Country)

        return countries

    @staticmethod
    def get(code: str) -> "Country | None":
        """Get a country by its code"""
        for country in Country.get_all():
            if country.country_code == code:
                return country
        return None

    @staticmethod
    def create(name: str, code: str) -> "Country":
        """Create a new country"""
        from src.persistence import repo

        country = Country(name, code)
        country.generate_id()

        repo.save(country)

        return country