"""
This module contains the routes for the users endpoints.
"""

from flask import Blueprint
from flask_jwt_extended import jwt_required
from src.controllers.users import (
    create_user,
    delete_user,
    get_user_by_id,
    get_users,
    update_user,
)

users_bp = Blueprint("users", __name__, url_prefix="/users")

users_bp.route("/", methods=["GET"])(get_users)
users_bp.route("/", methods=["POST"])(create_user)

users_bp.route("/<user_id>", methods=["GET"])(get_user_by_id)
users_bp.route("/<user_id>", methods=["PUT"])(jwt_required()(update_user))
users_bp.route("/<user_id>", methods=["DELETE"])(jwt_required()(delete_user))
