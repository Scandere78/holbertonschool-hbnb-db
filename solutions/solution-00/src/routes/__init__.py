""" """
from flask import jsonify
from flask_jwt_extended import jwt_required, get_jwt
from functools import wraps


def admin_required(fn):
    @wraps(fn)
    @jwt_required()
    def wrapper(*args, **kwargs):
        claims = get_jwt()
        is_admin = claims.get("is_admin", False)
        if not is_admin:
            return jsonify({ "message": "Forbidden!" }), 403
        return fn(*args, **kwargs)
    return wrapper
