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
    code = Column(String(3), nullable=False, unique=True)
    cities = relationship("City", back_populates="country")