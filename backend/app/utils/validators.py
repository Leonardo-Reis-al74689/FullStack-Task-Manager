"""Utilitários de validação e sanitização"""
import re
from typing import Optional

class InputValidator:
    """Classe para validação e sanitização de inputs"""
    
    @staticmethod
    def sanitize_string(value: str, max_length: Optional[int] = None) -> str:
        """
        Sanitiza uma string removendo caracteres perigosos
        
        Args:
            value: String a ser sanitizada
            max_length: Tamanho máximo permitido
            
        Returns:
            str: String sanitizada
        """
        if not isinstance(value, str):
            return ""
        
        sanitized = re.sub(r'[\x00-\x1f\x7f-\x9f]', '', value)
        sanitized = ' '.join(sanitized.split())
        
        if max_length and len(sanitized) > max_length:
            sanitized = sanitized[:max_length]
        
        return sanitized.strip()
    
    @staticmethod
    def validate_username(username: str) -> bool:
        """
        Valida formato de username
        
        Args:
            username: Username a ser validado
            
        Returns:
            bool: True se válido
        """
        if not username or len(username) < 3 or len(username) > 80:
            return False
        
        pattern = r'^[a-zA-Z0-9_-]+$'
        return bool(re.match(pattern, username))
    
    @staticmethod
    def validate_password_strength(password: str) -> bool:
        """
        Valida força da palavra-passe
        
        Args:
            password: Palavra-passe a ser validada
            
        Returns:
            bool: True se atende aos critérios mínimos
        """
        if not password or len(password) < 6:
            return False
        
        has_letter = bool(re.search(r'[a-zA-Z]', password))
        has_digit = bool(re.search(r'\d', password))
        
        return has_letter and has_digit
    
    @staticmethod
    def sanitize_html(value: str) -> str:
        """
        Remove tags HTML potencialmente perigosas e seu conteúdo
        
        Args:
            value: String que pode conter HTML
            
        Returns:
            str: String sem tags HTML e sem conteúdo de tags perigosas
        """
        if not isinstance(value, str):
            return ""
        
        sanitized = re.sub(r'<script[^>]*>.*?</script>', '', value, flags=re.DOTALL | re.IGNORECASE)
        sanitized = re.sub(r'<[^>]+>', '', sanitized)
        return sanitized.strip()

