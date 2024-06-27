"""
Amenity controller module
"""

from flask import abort, request
from src.models.amenity import Amenity
from src.models import get_class


def get_amenities():
    """Returns all amenities"""
    _cls = get_class("Amenity")
    amenities: list[Amenity] = _cls.get_all()

    return [amenity.to_dict() for amenity in amenities]


def create_amenity():
    """Creates a new amenity"""
    _cls = get_class("Amenity")
    data = request.get_json()

    try:
        amenity = _cls.create(data)
    except KeyError as e:
        abort(400, f"Missing field: {e}")
    except ValueError as e:
        abort(400, str(e))

    return amenity.to_dict(), 201


def get_amenity_by_id(amenity_id: str):
    """Returns a amenity by ID"""
    _cls = get_class("Amenity")
    amenity: Amenity | None = _cls.get(amenity_id)

    if not amenity:
        abort(404, f"Amenity with ID {amenity_id} not found")

    return amenity.to_dict()


def update_amenity(amenity_id: str):
    """Updates a amenity by ID"""
    _cls = get_class("Amenity")
    data = request.get_json()

    updated_amenity: Amenity | None = _cls.update(amenity_id, data)

    if not updated_amenity:
        abort(404, f"Amenity with ID {amenity_id} not found")

    return updated_amenity.to_dict()


def delete_amenity(amenity_id: str):
    """Deletes a amenity by ID"""
    _cls = get_class("Amenity")
    if not _cls.delete(amenity_id):
        abort(404, f"Amenity with ID {amenity_id} not found")

    return "", 204
