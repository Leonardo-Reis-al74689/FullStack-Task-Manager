"""Testes para error handler"""
import pytest
from app.middleware.error_handler import register_error_handlers
from app.exceptions.custom_exceptions import ResourceNotFoundException, ValidationException
from pydantic import ValidationError

@pytest.mark.unit
@pytest.mark.middleware
class TestErrorHandler:
    """Testes para error handlers"""
    
    def test_handle_not_found(self, app):
        """Testa handler para 404"""
        register_error_handlers(app)
        
        with app.test_client() as client:
            response = client.get('/rota-inexistente-12345')
            
            assert response.status_code == 404
            data = response.get_json()
            assert 'Rota não encontrada' in data['message']
    
    def test_handle_internal_error(self, app):
        """Testa handler para 500"""
        register_error_handlers(app)
        
        @app.route('/test-internal-error')
        def test_error():
            raise Exception("Internal server error")
        
        with app.test_client() as client:
            response = client.get('/test-internal-error')
            
            assert response.status_code == 500
            data = response.get_json()
            assert 'Erro interno do servidor' in data['message']
    
    def test_handle_app_exception(self, app):
        """Testa handler para AppException"""
        register_error_handlers(app)
        
        @app.route('/test-app-exception')
        def test_app_exception():
            raise ResourceNotFoundException(resource="Teste")
        
        with app.test_client() as client:
            response = client.get('/test-app-exception')
            
            assert response.status_code == 404
            data = response.get_json()
            assert 'Teste não encontrado' in data['message']
    
    def test_handle_validation_error(self, app):
        """Testa handler para ValidationError do Pydantic"""
        register_error_handlers(app)
        
        @app.route('/test-validation-error')
        def test_validation_error():
            from pydantic import ValidationError
            raise ValidationError.from_exception_data("TestModel", [])
        
        with app.test_client() as client:
            response = client.get('/test-validation-error')
            
            assert response.status_code in [400, 500]
    
    def test_handle_500_error_specifically(self, app):
        """Testa handler específico para erro 500"""
        register_error_handlers(app)
        
        @app.route('/test-500-error')
        def test_500_error():
            from flask import abort
            abort(500)
        
        with app.test_client() as client:
            response = client.get('/test-500-error')
            
            assert response.status_code == 500
            data = response.get_json()
            assert 'Erro interno do servidor' in data['message']
            assert data['error_code'] is not None

