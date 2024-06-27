"""
City related functionality
"""
from sqlalchemy import Column, String

from .base_model import BaseModel


class City(BaseModel):
    """City representation"""
    __tablename__ = "city"

    name = Column(String(120), nullable=False, unique=True)
    country_code = Column(String(3), nullable=False)