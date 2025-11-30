from enum import Enum

class TaskStatus(str, Enum):
    """Status possíveis de uma tarefa"""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    
    @classmethod
    def from_bool(cls, completed: bool) -> str:
        """Converte boolean para status"""
        return cls.COMPLETED if completed else cls.PENDING

