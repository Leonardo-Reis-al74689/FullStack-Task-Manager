from functools import wraps
from flask import jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.user import User
from app import db

def get_current_user():
    """Obtém o utilizador atual a partir do token JWT"""
    user_id = get_jwt_identity()
    return User.query.get(user_id)

def require_auth(f):
    """Decorator para rotas que requerem autenticação"""
    @wraps(f)
    @jwt_required()
    def decorated_function(*args, **kwargs):
        current_user = get_current_user()
        if not current_user:
            return jsonify({'message': 'Utilizador não encontrado'}), 404
        return f(current_user, *args, **kwargs)
    return decorated_function

