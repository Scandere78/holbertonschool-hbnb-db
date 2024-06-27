"""
  Now is easy to implement the database repository. The DBRepository
  should implement the Repository (Storage) interface and the methods defined
  in the abstract class Storage.

  The methods to implement are:
    - get_all
    - get
    - save
    - update
    - delete
    - reload (which can be empty)
"""
from flask_sqlalchemy import SQLAlchemy

from src.models.db.base_model import BaseModel
from src.persistence.repository import Repository
from src.db import db

class DBRepository(Repository):
    """Dummy DB repository"""
    db: SQLAlchemy

    def __init__(self) -> None:
        self.db = db

    def get_all(self, model) -> list:
        return db.session.query(model).all()

    def get(self, model, obj_id: str) -> BaseModel | None:
        """Get an object by its ID"""
        for obj in self.get_all(model):
            if obj.id == obj_id:
                return obj
        return None

    def reload(self) -> None:
        pass

    def save(self, obj) -> None:
        self.db.session.add(obj)
        self.db.session.commit()

    def update(self, obj) -> BaseModel | None:
        """Not implemented"""

    def delete(self, obj) -> bool:
        """Not implemented"""
        return False
