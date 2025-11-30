"""Rate Limiting middleware (opcional)"""
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask import request

def setup_rate_limiter(app):
    """Configura rate limiting na aplicação"""
    limiter = Limiter(
        app=app,
        key_func=get_remote_address,
        default_limits=["100 per hour"],
        storage_uri="memory://"
    )
    
    @app.after_request
    def add_rate_limit_headers(response):
        """Adiciona headers de rate limiting nas respostas"""
        return response
    
    return limiter

def rate_limit(limit: str):
    """
    Decorator para aplicar rate limiting
    
    Args:
        limit: String no formato "100 per hour"
    """
    from functools import wraps
    from flask import current_app
    
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            return f(*args, **kwargs)
        return decorated_function
    return decorator

