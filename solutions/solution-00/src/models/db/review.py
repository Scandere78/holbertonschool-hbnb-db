"""
Review related functionality
"""
from sqlalchemy import Column, String, Float

from .base_model import BaseModel


class Review(BaseModel):
    """User representation"""
    __tablename__ = "review"

    place_id = Column(String(60), nullable=False)
    user_id = Column(String(50), nullable=False)
    comment = Column(String, nullable=False)
    rating = Column(Float, nullable=False)