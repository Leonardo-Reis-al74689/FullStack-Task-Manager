"""Exceções customizadas para tratamento de erros padronizado"""
from app.enums.error_codes import ErrorCode
from app.enums.http_status import HTTPStatus

class AppException(Exception):
    """Classe base para todas as exceções da aplicação"""
    def __init__(
        self,
        message: str,
        error_code: ErrorCode,
        status_code: HTTPStatus = HTTPStatus.INTERNAL_SERVER_ERROR,
        details: dict = None
    ):
        self.message = message
        self.error_code = error_code
        self.status_code = status_code
        self.details = details or {}
        super().__init__(self.message)
    
    def to_dict(self):
        """Converte exceção para dicionário"""
        return {
            'message': self.message,
            'error_code': self.error_code.value,
            'status_code': self.status_code.value,
            'details': self.details
        }

class ValidationException(AppException):
    """Exceção para erros de validação"""
    def __init__(self, message: str = "Dados inválidos", details: dict = None):
        super().__init__(
            message=message,
            error_code=ErrorCode.VALIDATION_ERROR,
            status_code=HTTPStatus.BAD_REQUEST,
            details=details
        )

class AuthenticationException(AppException):
    """Exceção para erros de autenticação"""
    def __init__(self, message: str = "Credenciais inválidas", details: dict = None):
        super().__init__(
            message=message,
            error_code=ErrorCode.INVALID_CREDENTIALS,
            status_code=HTTPStatus.UNAUTHORIZED,
            details=details
        )

class AuthorizationException(AppException):
    """Exceção para erros de autorização"""
    def __init__(self, message: str = "Acesso não autorizado", details: dict = None):
        super().__init__(
            message=message,
            error_code=ErrorCode.UNAUTHORIZED_ACCESS,
            status_code=HTTPStatus.FORBIDDEN,
            details=details
        )

class ResourceNotFoundException(AppException):
    """Exceção para recursos não encontrados"""
    def __init__(self, resource: str = "Recurso", details: dict = None):
        super().__init__(
            message=f"{resource} não encontrado",
            error_code=ErrorCode.RESOURCE_NOT_FOUND,
            status_code=HTTPStatus.NOT_FOUND,
            details=details
        )

class ResourceAlreadyExistsException(AppException):
    """Exceção para recursos que já existem"""
    def __init__(self, resource: str = "Recurso", details: dict = None):
        super().__init__(
            message=f"{resource} já existe",
            error_code=ErrorCode.RESOURCE_ALREADY_EXISTS,
            status_code=HTTPStatus.CONFLICT,
            details=details
        )

class DatabaseException(AppException):
    """Exceção para erros de base de dados"""
    def __init__(self, message: str = "Erro na base de dados", details: dict = None):
        super().__init__(
            message=message,
            error_code=ErrorCode.DATABASE_ERROR,
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            details=details
        )

