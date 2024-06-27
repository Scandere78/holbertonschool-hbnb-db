"""
Amenity related functionality
"""
from sqlalchemy import Column, String

from .base_model import BaseModel


class Amenity(BaseModel):
    """Amenity representation"""
    __tablename__ = "amenities"

    name = Column(String(150), unique=True, nullable=False)

