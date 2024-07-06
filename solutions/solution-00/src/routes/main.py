"""
This module contains the routes for the authentification endpoint
"""
from flask_jwt_extended import jwt_required
from flask import Blueprint
from src.controllers.main import (
    post_login,
    get_protected,
    get_restricted
)
from src.routes import admin_required

main_bp = Blueprint("main", __name__, url_prefix="/")

main_bp.route("/login", methods=["POST"])(post_login)
main_bp.route("/protected", methods=["GET"])(jwt_required()(get_protected))
main_bp.route("/restricted", methods=["GET"])(admin_required(get_restricted))