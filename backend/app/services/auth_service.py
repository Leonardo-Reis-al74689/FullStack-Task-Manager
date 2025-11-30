"""Serviço de autenticação - Service Layer Pattern"""
from app import db
from app.models.user import User
from app.schemas.user import UserCreate, UserLogin
from app.utils.security import verify_password, get_password_hash
from app.exceptions.custom_exceptions import (
    AuthenticationException,
    ResourceAlreadyExistsException,
    DatabaseException
)
from flask_jwt_extended import create_access_token

class AuthService:
    """Classe de serviço para operações de autenticação"""
    
    @staticmethod
    def register_user(user_data: UserCreate) -> dict:
        """
        Regista um novo utilizador no sistema
        
        Args:
            user_data: Dados do utilizador para registo
            
        Returns:
            dict: Dados do utilizador criado
            
        Raises:
            ResourceAlreadyExistsException: Se utilizador ou email já existir
            DatabaseException: Se houver erro ao guardar na base de dados
        """
        existing_user = User.query.filter_by(username=user_data.username).first()
        if existing_user:
            raise ResourceAlreadyExistsException(
                resource="Nome de utilizador",
                details={"username": user_data.username}
            )
        
        existing_email = User.query.filter_by(email=user_data.email).first()
        if existing_email:
            raise ResourceAlreadyExistsException(
                resource="Email",
                details={"email": user_data.email}
            )
        
        try:
            new_user = User(
                username=user_data.username,
                email=user_data.email,
                hashed_password=get_password_hash(user_data.password)
            )
            db.session.add(new_user)
            db.session.commit()
            
            return new_user.to_dict()
        except Exception as e:
            db.session.rollback()
            raise DatabaseException(
                message="Erro ao criar utilizador na base de dados",
                details={"error": str(e)}
            )
    
    @staticmethod
    def authenticate_user(login_data: UserLogin) -> dict:
        """
        Autentica um utilizador e retorna token JWT
        
        Args:
            login_data: Dados de início de sessão (username e password)
            
        Returns:
            dict: Token JWT e dados do utilizador
            
        Raises:
            AuthenticationException: Se credenciais forem inválidas
        """
        user = User.query.filter_by(username=login_data.username).first()
        
        if not user or not verify_password(login_data.password, user.hashed_password):
            raise AuthenticationException(
                message="Credenciais inválidas",
                details={"username": login_data.username}
            )
        
        access_token = create_access_token(identity=user.id)
        
        return {
            'access_token': access_token,
            'token_type': 'bearer',
            'user': user.to_dict()
        }
    
    @staticmethod
    def get_user_by_id(user_id: int) -> User:
        """
        Busca utilizador por ID
        
        Args:
            user_id: ID do utilizador
            
        Returns:
            User: Objeto do utilizador
            
        Raises:
            ResourceNotFoundException: Se utilizador não for encontrado
        """
        from app.exceptions.custom_exceptions import ResourceNotFoundException
        
        user = User.query.get(user_id)
        if not user:
            raise ResourceNotFoundException(
                resource="Utilizador",
                details={"user_id": user_id}
            )
        return user

