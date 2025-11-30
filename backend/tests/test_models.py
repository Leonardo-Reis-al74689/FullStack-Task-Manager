"""Testes para modelos"""
import pytest
from app import db
from app.models.user import User
from app.models.task import Task
from app.utils.security import get_password_hash
from datetime import datetime

@pytest.mark.unit
class TestUserModel:
    """Testes para o modelo User"""
    
    def test_create_user(self, app):
        """Testa criação de utilizador"""
        with app.app_context():
            user = User(
                username='newuser',
                email='newuser@example.com',
                hashed_password=get_password_hash('password123')
            )
            db.session.add(user)
            db.session.commit()
            
            assert user.id is not None
            assert user.username == 'newuser'
            assert user.email == 'newuser@example.com'
            assert user.created_at is not None
    
    def test_user_to_dict(self, test_user):
        """Testa conversão de utilizador para dicionário"""
        user_dict = test_user.to_dict()
        
        assert 'id' in user_dict
        assert 'username' in user_dict
        assert 'email' in user_dict
        assert 'created_at' in user_dict
        assert user_dict['username'] == 'testuser'
        assert 'hashed_password' not in user_dict
    
    def test_user_repr(self, test_user):
        """Testa representação string do utilizador"""
        assert 'testuser' in str(test_user)

@pytest.mark.unit
class TestTaskModel:
    """Testes para o modelo Task"""
    
    def test_create_task(self, app, test_user):
        """Testa criação de tarefa"""
        with app.app_context():
            task = Task(
                title='Nova tarefa',
                description='Descrição',
                completed=False,
                user_id=test_user.id
            )
            db.session.add(task)
            db.session.commit()
            
            assert task.id is not None
            assert task.title == 'Nova tarefa'
            assert task.completed is False
            assert task.user_id == test_user.id
            assert task.created_at is not None
    
    def test_task_to_dict(self, test_task):
        """Testa conversão de tarefa para dicionário"""
        task_dict = test_task.to_dict()
        
        assert 'id' in task_dict
        assert 'title' in task_dict
        assert 'description' in task_dict
        assert 'completed' in task_dict
        assert 'created_at' in task_dict
        assert 'updated_at' in task_dict
        assert 'user_id' in task_dict
        assert task_dict['title'] == 'Tarefa de teste'
    
    def test_task_repr(self, test_task):
        """Testa representação string da tarefa"""
        assert 'Tarefa de teste' in str(test_task)
    
    def test_task_relationship_with_user(self, app, test_user):
        """Testa relacionamento entre tarefa e utilizador"""
        with app.app_context():
            task = Task(
                title='Tarefa relacionada',
                user_id=test_user.id
            )
            db.session.add(task)
            db.session.commit()
            db.session.refresh(task)
            
            user = db.session.get(User, test_user.id)
            
            assert task.user.id == test_user.id
            assert task.user.username == test_user.username
            assert task in user.tasks

