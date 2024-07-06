"""
Countries controller module
"""
from flask import abort, request
from flask_jwt_extended import create_access_token, get_jwt_identity

from src.app_bcrypt import bcrypt
from src.models.user import User
from src.models import get_class


def post_login():
    """Login a user."""
    email = request.json.get('email', None)
    password = request.json.get('password', None)

    _cls = get_class("User")
    users: list[User] | None = _cls.get_all()

    user: User = None
    for _user in users:
        if _user.email == email:
            user = _user

    if user and bcrypt.check_password_hash(user.password_hash, password):
        additional_claims = {"is_admin": user.is_admin}
        access_token = create_access_token(identity=user.id, additional_claims=additional_claims)
        return { "access_token": access_token }, 201

    abort(401, 'Wrong email or password')

def get_protected():
    """Retrieve a page for user logged, for test."""
    current_user = get_jwt_identity()
    return {
        'logged_in_as': current_user
    }

def get_restricted():
    """Retrieve a page for user logged ADMIN, for test."""
    current_user = get_jwt_identity()
    return {
        'logged_in_as': current_user,
        'is_admin': True
    }