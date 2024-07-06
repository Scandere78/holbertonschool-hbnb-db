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
from utils.populate import populate_db

class DBRepository(Repository):
    """Dummy DB repository"""
    db: SQLAlchemy

    def __init__(self) -> None:
        self.db = db
        self.reload()

    def get_all(self, model) -> list:
        """Get all objects of a given model"""
        return db.session.query(model).all()

    def get(self, model, obj_id: str) -> BaseModel | None:
        """Get an object by its ID"""
        for obj in self.get_all(model):
            if obj.id == obj_id:
                return obj
        return None

    def reload(self) -> None:
        """Populates the database with some dummy data"""
        populate_db(self)

    def save(self, obj) -> None:
        """Save an object to the repository"""
        self.db.session.add(obj)
        self.db.session.commit()

    def update(self, obj) -> BaseModel | None:
        """Update an object in the repository"""
        self.db.session.commit()

    def delete(self, obj) -> bool:
        """Delete an object from the repository"""
        try:
            self.db.session.delete(obj)
            self.db.session.commit()
            return True
        except Exception:
            return False
