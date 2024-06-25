"""
Country related functionality
"""
from src.models.base import Base
import uuid
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String, DateTime

class Country:
    """
    Country representation

    This class does NOT inherit from Base, you can't delete or update a country

    This class is used to get and list countries
    """
    id = Column(String(36), primary_key=True, default=uuid.uuid4)
    name = Column(String(120), nullable=False, unique=True)
    code = Column(String(3), nullable=False, unique=True)
    cities = relationship("City", back_populates="country")
    created_at = Column(DateTime, default=db.func.current_timestamp())
    updated_at = Column(DateTime, default=db.func.current_timestamp())

    def __init__(self, name: str, code: str, **kw) -> None:
        """Dummy init"""
        super().__init__(**kw)
        self.name = name
        self.code = code

    def __repr__(self) -> str:
        """Dummy repr"""
        return f"<Country {self.code} ({self.name})>"

    def to_dict(self) -> dict:
        """Returns the dictionary representation of the country"""
        return {
            "name": self.name,
            "code": self.code,
        }

    @staticmethod
    def get_all() -> list["Country"]:
        """Get all countries"""
        from src.persistence import repo

        countries: list["Country"] = repo.get_all("country")

        return countries

    @staticmethod
    def get(code: str) -> "Country | None":
        """Get a country by its code"""
        for country in Country.get_all():
            if country.code == code:
                return country
        return None

    @staticmethod
    def create(name: str, code: str) -> "Country":
        """Create a new country"""
        from src.persistence import repo

        country = Country(name, code)

        repo.save(country)

        return country
