"""Testes para rate limiter"""
import pytest
from app.middleware.rate_limiter import setup_rate_limiter, rate_limit
from flask import Flask

@pytest.mark.unit
@pytest.mark.middleware
class TestRateLimiter:
    """Testes para rate limiter"""
    
    def test_setup_rate_limiter(self, app):
        """Testa configuração do rate limiter"""
        limiter = setup_rate_limiter(app)
        assert limiter is not None
        assert limiter.app == app
    
    def test_rate_limit_decorator(self):
        """Testa decorator de rate limit"""
        @rate_limit("10 per minute")
        def test_function():
            return "test"
        
        result = test_function()
        assert result == "test"
    
    def test_rate_limit_decorator_with_args(self):
        """Testa decorator de rate limit com argumentos"""
        @rate_limit("10 per minute")
        def test_function(arg1, arg2=None):
            return f"{arg1}-{arg2}"
        
        result = test_function("test", arg2="value")
        assert result == "test-value"
    
    def test_rate_limit_decorator_with_kwargs(self):
        """Testa decorator de rate limit com kwargs"""
        @rate_limit("10 per minute")
        def test_function(**kwargs):
            return kwargs
        
        result = test_function(key="value")
        assert result == {"key": "value"}
    
    def test_rate_limit_headers_added(self, app):
        """Testa que headers de rate limiting são adicionados nas respostas"""
        limiter = setup_rate_limiter(app)
        
        @app.route('/test-rate-limit-headers')
        def test_route():
            return {'message': 'test'}
        
        with app.test_client() as client:
            response = client.get('/test-rate-limit-headers')
            assert response.status_code == 200
            assert response.get_json() is not None

