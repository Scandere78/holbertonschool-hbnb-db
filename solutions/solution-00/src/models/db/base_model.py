import datetime
from typing import Any
import uuid
from sqlalchemy import Column, String, DateTime

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
    created_at = Column(
        DateTime,
        default=datetime.datetime.utcnow
    )
    updated_at = Column(
        DateTime,
        default=datetime.datetime.utcnow,
        onupdate=datetime.datetime.utcnow
    )

    def generate_id(self):
        self.id = str(uuid.uuid4())

    @classmethod
    def get(cls, id) -> "Any | None":
        """
        This is a common method to get an specific object
        of a class by its id

        If a class needs a different implementation,
        it should override this method
        """
        from src.persistence import repo

        return repo.get(cls, id)

    @classmethod
    def get_all(cls) -> list["Any"]:
        """
        This is a common method to get all objects of a class

        If a class needs a different implementation,
        it should override this method
        """
        from src.persistence import repo

        return repo.get_all(cls)

    @classmethod
    def delete(cls, id) -> bool:
        """
        This is a common method to delete an specific
        object of a class by its id

        If a class needs a different implementation,
        it should override this method
        """
        from src.persistence import repo

        obj = cls.get(id)

        if not obj:
            return False

        return repo.delete(obj)

    def to_dict(self):
        result = {}
        for key, value in self.__dict__.items():
            if isinstance(value, datetime.datetime):
                result[key] = value.isoformat()
            else:
                result[key] = value
        return result