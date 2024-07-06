""" """
from flask_jwt_extended import get_jwt_identity, get_jwt

def get_jwt_data():
    claims = get_jwt()
    jwt_id = get_jwt_identity()

    is_admin = claims.get("is_admin", False)

    return jwt_id, is_admin