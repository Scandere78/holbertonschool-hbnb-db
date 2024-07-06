"""
user related functionality
"""
from copy import copy
import uuid
from sqlalchemy import Column, String, Boolean

from .base_model import BaseModel
from src.app_bcrypt import generate_password, check_password


class User(BaseModel):
    """User representation"""
    __tablename__ = "user"

    email = Column(String(120), unique=True, nullable=False)
    first_name = Column(String(120), nullable=False)
    last_name = Column(String(120), nullable=False)
    password_hash = Column(String(128))
    is_admin = Column(Boolean, default=False)

    def __repr__(self) -> str:
        """Dummy repr"""
        return f"<User {self.id} ({self.email})>"

    def set_password(self, password):
        self.password_hash = generate_password(password)

    def check_password(self, password):
        return check_password(self.password_hash, password)

    def to_dict(self) -> dict:
        """Dictionary representation of the object"""
        return {
            "id": self.id,
            "email": self.email,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "password_hash": self.password_hash,
            "is_admin": self.is_admin,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }

    @staticmethod
    def create(user: dict) -> "User":
        """Create a new user"""
        from src.persistence import repo

        users: list["User"] = User.get_all()

        for u in users:
            if u.email == user["email"]:
                raise ValueError("User already exists")

        user['password_hash'] = None
        password = copy(user['password'])
        del user['password']

        new_user = User(**user)
        new_user.set_password(password)
        new_user.id = str(uuid.uuid4())

        repo.save(new_user)

        return new_user

    @staticmethod
    def update(user_id: str, data: dict) -> "User | None":
        """Update an existing user"""
        from src.persistence import repo

        user: User | None = User.get(user_id)

        if not user:
            return None

        if "email" in data:
            user.email = data["email"]
        if "first_name" in data:
            user.first_name = data["first_name"]
        if "last_name" in data:
            user.last_name = data["last_name"]

        repo.update(user)

        return user