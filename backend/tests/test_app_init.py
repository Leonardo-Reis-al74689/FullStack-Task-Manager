"""Testes para inicialização da aplicação"""
import pytest
import sys
import os
from app import create_app, db
from config import Config

class TestConfigWithRateLimit(Config):
    """Configuração de teste com rate limit habilitado"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    JWT_SECRET_KEY = 'test-jwt-secret-key'
    SECRET_KEY = 'test-secret-key'
    WTF_CSRF_ENABLED = False
    RATELIMIT_ENABLED = True

@pytest.mark.unit
@pytest.mark.app
class TestAppInit:
    """Testes para inicialização da aplicação"""
    
    def test_create_app_with_rate_limit(self):
        """Testa criação da aplicação com rate limit habilitado"""
        app = create_app(TestConfigWithRateLimit)
        assert app is not None
        assert app.config['RATELIMIT_ENABLED'] is True
    
    def test_create_app_without_rate_limit(self):
        """Testa criação da aplicação sem rate limit"""
        from config import Config
        
        class TestConfigNoRateLimit(Config):
            TESTING = True
            SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
            JWT_SECRET_KEY = 'test-jwt-secret-key'
            SECRET_KEY = 'test-secret-key'
            WTF_CSRF_ENABLED = False
            RATELIMIT_ENABLED = False
        
        app = create_app(TestConfigNoRateLimit)
        assert app is not None
        assert app.config.get('RATELIMIT_ENABLED', False) is False
    
    def test_sys_path_insertion(self):
        """Testa que parent_dir é adicionado ao sys.path quando não está presente"""
        import importlib
        import types
        
        app_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'app', '__init__.py')
        app_dir = os.path.dirname(app_file)
        parent_dir = os.path.dirname(app_dir)
        
        was_in_path = parent_dir in sys.path
        
        if was_in_path:
            sys.path.remove(parent_dir)
        
        app_module = sys.modules.get('app')
        config_module = sys.modules.get('config')
        
        modules_to_remove = []
        for mod_name in list(sys.modules.keys()):
            if mod_name.startswith('app') or mod_name == 'config':
                modules_to_remove.append((mod_name, sys.modules[mod_name]))
                del sys.modules[mod_name]
        
        try:
            assert parent_dir not in sys.path, "parent_dir já está no sys.path"
            
            with open(app_file, 'r', encoding='utf-8') as f:
                code = f.read()
            
            namespace = {
                '__file__': app_file,
                '__name__': 'app',
                '__package__': '',
            }
            
            exec(compile(code, app_file, 'exec'), namespace)
            
            assert parent_dir in sys.path, "parent_dir não foi adicionado ao sys.path pela linha 10"
            
        finally:
            for mod_name, mod_obj in modules_to_remove:
                sys.modules[mod_name] = mod_obj
            
            if not was_in_path and parent_dir in sys.path:
                sys.path.remove(parent_dir)
            elif was_in_path and parent_dir not in sys.path:
                sys.path.insert(0, parent_dir)

