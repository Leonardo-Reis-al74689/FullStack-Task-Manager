"""Testes para TaskStatus"""
import pytest
from app.enums.task_status import TaskStatus

@pytest.mark.unit
@pytest.mark.enums
class TestTaskStatus:
    """Testes para TaskStatus enum"""
    
    def test_from_bool_completed(self):
        """Testa conversão de boolean True para status"""
        result = TaskStatus.from_bool(True)
        assert result == TaskStatus.COMPLETED
    
    def test_from_bool_pending(self):
        """Testa conversão de boolean False para status"""
        result = TaskStatus.from_bool(False)
        assert result == TaskStatus.PENDING

