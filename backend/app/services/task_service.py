"""Serviço de tarefas - Service Layer Pattern"""
from typing import List, Optional
from app import db
from app.models.task import Task
from app.models.user import User
from app.schemas.task import TaskCreate, TaskUpdate
from app.exceptions.custom_exceptions import (
    ResourceNotFoundException,
    AuthorizationException,
    DatabaseException
)

class TaskService:
    """Classe de serviço para operações com tarefas"""
    
    @staticmethod
    def get_user_tasks(user: User) -> List[Task]:
        """
        Lista todas as tarefas de um utilizador
        
        Args:
            user: Utilizador autenticado
            
        Returns:
            List[Task]: Lista de tarefas do utilizador
        """
        return Task.query.filter_by(user_id=user.id).order_by(Task.created_at.desc()).all()
    
    @staticmethod
    def get_task_by_id(task_id: int, user: User) -> Task:
        """
        Busca uma tarefa específica do utilizador
        
        Args:
            task_id: ID da tarefa
            user: Utilizador autenticado
            
        Returns:
            Task: Objeto da tarefa
            
        Raises:
            ResourceNotFoundException: Se tarefa não for encontrada
            AuthorizationException: Se tarefa não pertencer ao utilizador
        """
        task = Task.query.filter_by(id=task_id).first()
        
        if not task:
            raise ResourceNotFoundException(
                resource="Tarefa",
                details={"task_id": task_id}
            )
        
        if task.user_id != user.id:
            raise AuthorizationException(
                message="Não tem permissão para aceder a esta tarefa",
                details={"task_id": task_id, "user_id": user.id}
            )
        
        return task
    
    @staticmethod
    def create_task(task_data: TaskCreate, user: User) -> Task:
        """
        Cria uma nova tarefa para o utilizador
        
        Args:
            task_data: Dados da tarefa
            user: Utilizador autenticado
            
        Returns:
            Task: Tarefa criada
            
        Raises:
            DatabaseException: Se houver erro ao guardar na base de dados
        """
        try:
            new_task = Task(
                title=task_data.title,
                description=task_data.description,
                completed=task_data.completed,
                user_id=user.id
            )
            db.session.add(new_task)
            db.session.commit()
            db.session.refresh(new_task)
            return new_task
        except Exception as e:
            db.session.rollback()
            raise DatabaseException(
                message="Erro ao criar tarefa na base de dados",
                details={"error": str(e)}
            )
    
    @staticmethod
    def update_task(task_id: int, task_data: TaskUpdate, user: User) -> Task:
        """
        Atualiza uma tarefa existente
        
        Args:
            task_id: ID da tarefa
            task_data: Dados para atualização
            user: Utilizador autenticado
            
        Returns:
            Task: Tarefa atualizada
            
        Raises:
            ResourceNotFoundException: Se tarefa não for encontrada
            AuthorizationException: Se tarefa não pertencer ao utilizador
            DatabaseException: Se houver erro ao atualizar na base de dados
        """
        task = TaskService.get_task_by_id(task_id, user)
        
        try:
            if task_data.title is not None:
                task.title = task_data.title
            if task_data.description is not None:
                task.description = task_data.description
            if task_data.completed is not None:
                task.completed = task_data.completed
            
            db.session.commit()
            db.session.refresh(task)
            return task
        except Exception as e:
            db.session.rollback()
            raise DatabaseException(
                message="Erro ao atualizar tarefa na base de dados",
                details={"error": str(e)}
            )
    
    @staticmethod
    def delete_task(task_id: int, user: User) -> None:
        """
        Elimina uma tarefa
        
        Args:
            task_id: ID da tarefa
            user: Utilizador autenticado
            
        Raises:
            ResourceNotFoundException: Se tarefa não for encontrada
            AuthorizationException: Se tarefa não pertencer ao utilizador
            DatabaseException: Se houver erro ao eliminar na base de dados
        """
        task = TaskService.get_task_by_id(task_id, user)
        
        try:
            db.session.delete(task)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise DatabaseException(
                message="Erro ao eliminar tarefa na base de dados",
                details={"error": str(e)}
            )

