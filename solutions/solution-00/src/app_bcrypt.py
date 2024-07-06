from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

def generate_password(password: str):
    return bcrypt.generate_password_hash(password).decode('utf-8')

def check_password(password_hash: str, password_to_check: str):
    return bcrypt.check_password_hash(password_hash, password_to_check)
