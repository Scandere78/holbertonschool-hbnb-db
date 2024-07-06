"""
Review related functionality
"""
from sqlalchemy import Column, String, Float, ForeignKey

from src.models.db.place import Place
from src.models.db.user import User
from .base_model import BaseModel


class Review(BaseModel):
    """Review representation"""
    __tablename__ = "review"

    place_id = Column(String(256), ForeignKey(Place.id), nullable=False)
    user_id = Column(String(256), ForeignKey(User.id), nullable=False)
    comment = Column(String, nullable=False)
    rating = Column(Float, nullable=False)

    def __repr__(self) -> str:
        """Dummy repr"""
        return f"<Review {self.id} - '{self.comment[:25]}...'>"

    def to_dict(self) -> dict:
        """Dictionary representation of the object"""
        return {
            "id": self.id,
            "place_id": self.place_id,
            "user_id": self.user_id,
            "comment": self.comment,
            "rating": self.rating,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }

    @staticmethod
    def create(data: dict) -> "Review":
        """Create a new review"""
        from src.persistence import repo

        user: User | None = User.get(data["user_id"])

        if not user:
            raise ValueError(f"User with ID {data['user_id']} not found")

        place: Place | None = Place.get(data["place_id"])

        if not place:
            raise ValueError(f"Place with ID {data['place_id']} not found")

        new_review = Review(**data)
        new_review.generate_id()

        repo.save(new_review)

        return new_review

    @staticmethod
    def update(review_id: str, data: dict) -> "Review | None":
        """Update an existing review"""
        from src.persistence import repo

        review = Review.get(review_id)

        if not review:
            raise ValueError("Review not found")

        for key, value in data.items():
            setattr(review, key, value)

        repo.update(review)

        return review