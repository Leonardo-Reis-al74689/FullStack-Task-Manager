from pydantic import BaseModel, Field, model_validator
from typing import Optional

class TaskCreate(BaseModel):
    """Schema para criação de tarefa"""
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    completed: bool = False

class TaskUpdate(BaseModel):
    """Schema para atualização de tarefa"""
    title: Optional[str] = Field(default=None, min_length=1, max_length=200)
    description: Optional[str] = None
    completed: Optional[bool] = None
    
    @model_validator(mode='before')
    @classmethod
    def validate_title_not_none(cls, data):
        """Valida que title não seja None se fornecido explicitamente"""
        if isinstance(data, dict) and 'title' in data and data['title'] is None:
            raise ValueError('title não pode ser None')
        return data

class TaskResponse(BaseModel):
    """Schema de resposta da tarefa"""
    id: int
    title: str
    description: Optional[str]
    completed: bool
    created_at: str
    updated_at: str
    user_id: int
    
    class Config:
        from_attributes = True

