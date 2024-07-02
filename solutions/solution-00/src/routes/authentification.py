from flask import abort, jsonify, request
from app import app
from app_bcrypt import bcrypt
from flask_jwt_extended import create_access_token
from src.models import get_class
from src.models.user import User




@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username', None)
    password = request.json.get('password', None)
    _cls = get_class("User")
    user: User | None = _cls.get(username)
    if user and bcrypt.check_password_hash(user.password, password):
        access_token = create_access_token(identity=username)
        return jsonify(access_token=access_token), 200
    return 'Wrong username or password', 401