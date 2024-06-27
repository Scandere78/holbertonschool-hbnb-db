"""
Cities controller module
"""

from flask import request, abort
from src.models.city import City
from src.models import get_class


def get_cities():
    """Returns all cities"""
    _cls = get_class("City")
    cities: list[City] = _cls.get_all()

    return [city.to_dict() for city in cities]


def create_city():
    """Creates a new city"""
    _cls = get_class("City")
    data = request.get_json()

    try:
        city = _cls.create(data)
    except KeyError as e:
        abort(400, f"Missing field: {e}")
    except ValueError as e:
        abort(400, str(e))

    return city.to_dict(), 201


def get_city_by_id(city_id: str):
    """Returns a city by ID"""
    _cls = get_class("City")
    city: City | None = _cls.get(city_id)

    if not city:
        abort(404, f"City with ID {city_id} not found")

    return city.to_dict()


def update_city(city_id: str):
    """Updates a city by ID"""
    _cls = get_class("City")
    data = request.get_json()

    try:
        city: City | None = _cls.update(city_id, data)
    except ValueError as e:
        abort(400, str(e))

    if not city:
        abort(404, f"City with ID {city_id} not found")

    return city.to_dict()


def delete_city(city_id: str):
    """Deletes a city by ID"""
    _cls = get_class("City")
    if not _cls.delete(city_id):
        abort(404, f"City with ID {city_id} not found")

    return "", 204
