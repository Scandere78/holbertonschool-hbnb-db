import datetime
import uuid
from sqlalchemy import Column, String, Integer, DateTime

from src.db import db


class BaseModel(db.Model):
    """ Base class for all models """
    __abstract__ = True

    id = Column(
        String(256),
        unique=True,
        nullable=False,
        default=str(uuid.uuid4()),
        primary_key=True
    )
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow,
                        onupdate=datetime.datetime.utcnow)

    def save(self):

        db.session.add(self)
        db.session.commit()

    def delete(self):

        db.session.delete(self)
        db.session.commit()

    def to_dict(self):
        result = {}
        for key, value in self.__dict__.items():
            if isinstance(value, datetime.datetime):
                result[key] = value.isoformat()
            else:
                result[key] = value
        return result