"""
Places controller module
"""

from flask import abort, request
from src.models.place import Place
from src.models import get_class


def get_places():
    """Returns all places"""
    _cls = get_class("Place")
    places: list[Place] = _cls.get_all()

    return [place.to_dict() for place in places], 200


def create_place():
    """Creates a new place"""
    _cls = get_class("Place")
    data = request.get_json()

    try:
        place = _cls.create(data)
    except KeyError as e:
        abort(400, f"Missing field: {e}")
    except ValueError as e:
        abort(404, str(e))

    return place.to_dict(), 201


def get_place_by_id(place_id: str):
    """Returns a place by ID"""
    _cls = get_class("Place")
    place: Place | None = _cls.get(place_id)

    if not place:
        abort(404, f"Place with ID {place_id} not found")

    return place.to_dict(), 200


def update_place(place_id: str):
    """Updates a place by ID"""
    _cls = get_class("Place")
    data = request.get_json()

    try:
        place: Place | None = _cls.update(place_id, data)
    except ValueError as e:
        abort(400, str(e))

    if not place:
        abort(404, f"Place with ID {place_id} not found")

    return place.to_dict(), 200


def delete_place(place_id: str):
    """Deletes a place by ID"""
    _cls = get_class("Place")
    if not _cls.delete(place_id):
        abort(404, f"Place with ID {place_id} not found")

    return "", 204
