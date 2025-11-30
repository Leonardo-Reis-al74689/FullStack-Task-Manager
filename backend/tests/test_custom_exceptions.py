"""Testes para custom exceptions"""
import pytest
from app.exceptions.custom_exceptions import (
    ValidationException,
    DatabaseException,
    AppException
)
from app.enums.error_codes import ErrorCode
from app.enums.http_status import HTTPStatus

@pytest.mark.unit
@pytest.mark.exceptions
class TestCustomExceptions:
    """Testes para exceções customizadas"""
    
    def test_validation_exception_default(self):
        """Testa ValidationException com valores padrão"""
        exc = ValidationException()
        assert exc.message == "Dados inválidos"
        assert exc.error_code == ErrorCode.VALIDATION_ERROR
        assert exc.status_code == HTTPStatus.BAD_REQUEST
    
    def test_validation_exception_custom(self):
        """Testa ValidationException com mensagem customizada"""
        exc = ValidationException(message="Campo obrigatório", details={"field": "email"})
        assert exc.message == "Campo obrigatório"
        assert exc.details == {"field": "email"}
    
    def test_database_exception_default(self):
        """Testa DatabaseException com valores padrão"""
        exc = DatabaseException()
        assert exc.message == "Erro na base de dados"
        assert exc.error_code == ErrorCode.DATABASE_ERROR
        assert exc.status_code == HTTPStatus.INTERNAL_SERVER_ERROR
    
    def test_database_exception_custom(self):
        """Testa DatabaseException com mensagem customizada"""
        exc = DatabaseException(message="Erro ao conectar", details={"error": "timeout"})
        assert exc.message == "Erro ao conectar"
        assert exc.details == {"error": "timeout"}
    
    def test_app_exception_to_dict(self):
        """Testa conversão de exceção para dicionário"""
        exc = AppException(
            message="Teste",
            error_code=ErrorCode.VALIDATION_ERROR,
            status_code=HTTPStatus.BAD_REQUEST,
            details={"key": "value"}
        )
        
        result = exc.to_dict()
        assert result['message'] == "Teste"
        assert result['error_code'] == ErrorCode.VALIDATION_ERROR.value
        assert result['status_code'] == HTTPStatus.BAD_REQUEST.value
        assert result['details'] == {"key": "value"}

