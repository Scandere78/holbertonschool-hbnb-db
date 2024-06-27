"""
user related functionality
"""
from sqlalchemy import Column, String

from .base_model import BaseModel


class User(BaseModel):
    """User representation"""
    __tablename__ = "user"

    email = Column(String(120), unique=True, nullable=False)
    first_name = Column(String(120), nullable=False)
    last_name = Column(String(120), nullable=False)