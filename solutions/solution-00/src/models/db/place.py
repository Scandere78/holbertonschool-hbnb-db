"""
Place related functionality
"""
from sqlalchemy import Column, String, Float, ForeignKey, Integer

from .base_model import BaseModel


class Place(BaseModel):
    """Place representation"""
    __tablename__ = "Place"

    name = Column(String(120), nullable=False, unique=True)
    description = Column(String, nullable=False)
    address = Column(String, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    host_id = Column(String(36), ForeignKey('user.id'), nullable=False)
    city_id = Column(String(36), ForeignKey('city.id'), nullable=False)
    price_per_night = Column(Integer, nullable=False)
    number_of_rooms = Column(Integer, nullable=False)
    number_of_bathrooms = Column(Integer, nullable=False)
    max_guests = Column(Integer, nullable=False)