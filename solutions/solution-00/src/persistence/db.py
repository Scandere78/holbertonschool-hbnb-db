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

from src.models.base import Base
from src.persistence.repository import Repository
from ..db import db

class DBRepository(Repository):
    """Dummy DB repository"""
    db: SQLAlchemy

    def __init__(self) -> None:
        self.db = db
        print(self.db)

    def get_all(self, model_name: str) -> list:
        return db.session.query(model_name)

    def get(self, model_name: str, obj_id: str) -> Base | None:
        """Not implemented"""

    def reload(self) -> None:
        """Not implemented"""

    def save(self, obj: Base) -> None:
        """Not implemented"""

    def update(self, obj: Base) -> Base | None:
        """Not implemented"""

    def delete(self, obj: Base) -> bool:
        """Not implemented"""
        return False
