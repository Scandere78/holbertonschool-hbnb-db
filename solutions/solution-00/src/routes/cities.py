"""
This module contains the routes for the cities blueprint
"""

from flask import Blueprint
from src.controllers.cities import (
    create_city,
    delete_city,
    get_city_by_id,
    get_cities,
    update_city,
)
from src.routes import admin_required

cities_bp = Blueprint("cities", __name__, url_prefix="/cities")

cities_bp.route("/", methods=["GET"])(get_cities)
cities_bp.route("/", methods=["POST"])(admin_required(create_city))

cities_bp.route("/<city_id>", methods=["GET"])(get_city_by_id)
cities_bp.route("/<city_id>", methods=["PUT"])(admin_required(update_city))
cities_bp.route("/<city_id>", methods=["DELETE"])(admin_required(delete_city))
