"""
Users controller module
"""

from flask import abort, request

from src.controllers import get_jwt_data
from src.models.user import User
from src.models import get_class


def get_users():
    """Returns all users"""
    _cls = get_class("User")
    users: list[User] = _cls.get_all()

    return [user.to_dict() for user in users]


def create_user():
    """Creates a new user"""
    _cls = get_class("User")
    data = request.get_json()

    try:
        user = _cls.create(data)
    except KeyError as e:
        abort(400, f"Missing field: {e}")
    except ValueError as e:
        abort(400, str(e))

    if user is None:
        abort(400, "User already exists")

    return user.to_dict(), 201


def get_user_by_id(user_id: str):
    """Returns a user by ID"""
    _cls = get_class("User")
    user: User | None = _cls.get(user_id)

    if not user:
        abort(404, f"User with ID {user_id} not found")

    return user.to_dict(), 200


def update_user(user_id: str):
    """Updates a user by ID"""
    current_user, is_admin = get_jwt_data()

    _cls = get_class("User")
    data = request.get_json()

    if not is_admin:
        if user_id != current_user:
            abort(403, f"Prohibited to update this user.")

    try:
        user = _cls.update(user_id, data)
    except ValueError as e:
        abort(400, str(e))

    if user is None:
        abort(404, f"User with ID {user_id} not found")

    return user.to_dict(), 200


def delete_user(user_id: str):
    """Deletes a user by ID"""
    current_user, is_admin = get_jwt_data()

    if not is_admin:
        if user_id != current_user:
            abort(403, f"Prohibited to delete this user.")

    _cls = get_class("User")
    if not _cls.delete(user_id):
        abort(404, f"User with ID {user_id} not found")

    return "", 204
