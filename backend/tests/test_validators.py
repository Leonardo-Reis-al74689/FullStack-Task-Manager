"""Testes para validators"""
import pytest
from app.utils.validators import InputValidator

@pytest.mark.unit
@pytest.mark.validators
class TestInputValidator:
    """Testes para InputValidator"""
    
    def test_sanitize_string_basic(self):
        """Testa sanitização básica de string"""
        result = InputValidator.sanitize_string("  teste  ")
        assert result == "teste"
    
    def test_sanitize_string_remove_control_chars(self):
        """Testa remoção de caracteres de controle"""
        result = InputValidator.sanitize_string("teste\x00\x1f\x7f\x9f")
        assert result == "teste"
    
    def test_sanitize_string_multiple_spaces(self):
        """Testa normalização de múltiplos espaços"""
        result = InputValidator.sanitize_string("teste    com    espaços")
        assert result == "teste com espaços"
    
    def test_sanitize_string_with_max_length(self):
        """Testa sanitização com limite de tamanho"""
        result = InputValidator.sanitize_string("teste muito longo", max_length=5)
        assert result == "teste"
    
    def test_sanitize_string_not_string(self):
        """Testa sanitização de valor que não é string"""
        result = InputValidator.sanitize_string(123)
        assert result == ""
    
    def test_sanitize_string_none(self):
        """Testa sanitização de None"""
        result = InputValidator.sanitize_string(None)
        assert result == ""
    
    def test_validate_username_valid(self):
        """Testa validação de username válido"""
        assert InputValidator.validate_username("user123") is True
        assert InputValidator.validate_username("user_name") is True
        assert InputValidator.validate_username("user-name") is True
        assert InputValidator.validate_username("abc") is True
        assert InputValidator.validate_username("a" * 80) is True
    
    def test_validate_username_invalid_short(self):
        """Testa validação de username muito curto"""
        assert InputValidator.validate_username("ab") is False
        assert InputValidator.validate_username("") is False
    
    def test_validate_username_invalid_long(self):
        """Testa validação de username muito longo"""
        assert InputValidator.validate_username("a" * 81) is False
    
    def test_validate_username_invalid_chars(self):
        """Testa validação de username com caracteres inválidos"""
        assert InputValidator.validate_username("user@name") is False
        assert InputValidator.validate_username("user name") is False
        assert InputValidator.validate_username("user.name") is False
        assert InputValidator.validate_username("user!name") is False
    
    def test_validate_username_none(self):
        """Testa validação de username None"""
        assert InputValidator.validate_username(None) is False
    
    def test_validate_password_strength_valid(self):
        """Testa validação de palavra-passe forte válida"""
        assert InputValidator.validate_password_strength("pass123") is True
        assert InputValidator.validate_password_strength("PASS123") is True
        assert InputValidator.validate_password_strength("123abc") is True
    
    def test_validate_password_strength_invalid_short(self):
        """Testa validação de palavra-passe muito curta"""
        assert InputValidator.validate_password_strength("pass1") is False
        assert InputValidator.validate_password_strength("") is False
    
    def test_validate_password_strength_invalid_no_letter(self):
        """Testa validação de palavra-passe sem letras"""
        assert InputValidator.validate_password_strength("123456") is False
    
    def test_validate_password_strength_invalid_no_digit(self):
        """Testa validação de palavra-passe sem dígitos"""
        assert InputValidator.validate_password_strength("password") is False
    
    def test_validate_password_strength_none(self):
        """Testa validação de palavra-passe None"""
        assert InputValidator.validate_password_strength(None) is False
    
    def test_sanitize_html_basic(self):
        """Testa sanitização básica de HTML"""
        result = InputValidator.sanitize_html("<script>alert('xss')</script>teste")
        assert result == "teste"
    
    def test_sanitize_html_multiple_tags(self):
        """Testa remoção de múltiplas tags HTML"""
        result = InputValidator.sanitize_html("<p>teste</p><div>conteúdo</div>")
        assert result == "testeconteúdo"
    
    def test_sanitize_html_no_tags(self):
        """Testa sanitização de string sem tags"""
        result = InputValidator.sanitize_html("texto simples")
        assert result == "texto simples"
    
    def test_sanitize_html_not_string(self):
        """Testa sanitização de valor que não é string"""
        result = InputValidator.sanitize_html(123)
        assert result == ""
    
    def test_sanitize_html_none(self):
        """Testa sanitização de None"""
        result = InputValidator.sanitize_html(None)
        assert result == ""

