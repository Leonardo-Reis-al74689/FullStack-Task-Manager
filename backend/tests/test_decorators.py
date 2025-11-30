"""Testes para decorators"""
import pytest
from unittest.mock import patch, MagicMock
from app.utils.decorators import get_current_user, require_auth
from app.models.user import User
from flask_jwt_extended import create_access_token

@pytest.mark.unit
@pytest.mark.decorators
class TestDecorators:
    """Testes para decorators"""
    
    def test_get_current_user_success(self, app, test_user):
        """Testa obtenção de utilizador atual"""
        with app.app_context():
            with patch('app.utils.decorators.get_jwt_identity', return_value=test_user.id):
                user = get_current_user()
                assert user is not None
                assert user.id == test_user.id
    
    def test_get_current_user_not_found(self, app):
        """Testa get_current_user quando utilizador não é encontrado"""
        with app.app_context():
            with patch('app.utils.decorators.get_jwt_identity', return_value=99999):
                user = get_current_user()
                assert user is None
    
    def test_require_auth_user_not_found(self, app):
        """Testa require_auth quando utilizador não é encontrado na base de dados"""
        with app.app_context():
            non_existent_user_id = 99999
            token = create_access_token(identity=non_existent_user_id)
            
            @app.route('/test-require-auth-not-found')
            @require_auth
            def test_route(current_user):
                return {'message': 'success'}
            
            with app.test_client() as client:
                response = client.get(
                    '/test-require-auth-not-found',
                    headers={'Authorization': f'Bearer {token}'}
                )
                
                assert response.status_code == 404
                data = response.get_json()
                assert 'Utilizador não encontrado' in data['message']

