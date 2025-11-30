from flask import Blueprint, request, jsonify
from app.schemas.task import TaskCreate, TaskUpdate
from app.services.task_service import TaskService
from app.utils.decorators import require_auth
from app.middleware.security_headers import validate_json_content_type
from app.enums.http_status import HTTPStatus
from pydantic import ValidationError

tasks_bp = Blueprint('tasks', __name__)

@tasks_bp.route('', methods=['GET'])
@require_auth
def list_tasks(current_user):
    """Rota privada para listar tarefas do utilizador atual"""
    try:
        tasks = TaskService.get_user_tasks(current_user)
        
        return jsonify({
            'message': 'Tarefas listadas com sucesso',
            'tasks': [task.to_dict() for task in tasks],
            'total': len(tasks)
        }), HTTPStatus.OK.value
    except Exception as e:
        raise

@tasks_bp.route('', methods=['POST'])
@require_auth
@validate_json_content_type
def create_task(current_user):
    """Rota privada para criar nova tarefa"""
    try:
        data = request.get_json()
        task_data = TaskCreate(**data)
        
        new_task = TaskService.create_task(task_data, current_user)
        
        return jsonify({
            'message': 'Tarefa criada com sucesso',
            'task': new_task.to_dict()
        }), HTTPStatus.CREATED.value
        
    except ValidationError as e:
        raise
    except Exception as e:
        raise

@tasks_bp.route('/<int:task_id>', methods=['GET'])
@require_auth
def get_task(current_user, task_id):
    """Rota privada para obter uma tarefa específica"""
    try:
        task = TaskService.get_task_by_id(task_id, current_user)
        
        return jsonify({
            'message': 'Tarefa encontrada',
            'task': task.to_dict()
        }), HTTPStatus.OK.value
    except Exception as e:
        raise

@tasks_bp.route('/<int:task_id>', methods=['PUT'])
@require_auth
@validate_json_content_type
def update_task(current_user, task_id):
    """Rota privada para atualizar uma tarefa"""
    try:
        data = request.get_json()
        task_data = TaskUpdate(**data)
        
        updated_task = TaskService.update_task(task_id, task_data, current_user)
        
        return jsonify({
            'message': 'Tarefa atualizada com sucesso',
            'task': updated_task.to_dict()
        }), HTTPStatus.OK.value
        
    except ValidationError as e:
        raise
    except Exception as e:
        raise

@tasks_bp.route('/<int:task_id>', methods=['DELETE'])
@require_auth
def delete_task(current_user, task_id):
    """Rota privada para eliminar uma tarefa"""
    try:
        TaskService.delete_task(task_id, current_user)
        
        return jsonify({
            'message': 'Tarefa eliminada com sucesso'
        }), HTTPStatus.OK.value
    except Exception as e:
        raise

