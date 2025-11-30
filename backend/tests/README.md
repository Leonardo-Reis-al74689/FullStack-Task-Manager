# Testes do Backend

Suite completa de testes para o backend Flask usando pytest.

## 📋 Estrutura de Testes

```
tests/
├── __init__.py
├── conftest.py              # Fixtures e configuração
├── test_models.py           # Testes dos modelos
├── test_auth_service.py     # Testes do serviço de autenticação
├── test_task_service.py     # Testes do serviço de tarefas
├── test_auth_routes.py      # Testes das rotas de autenticação
└── test_task_routes.py      # Testes das rotas de tarefas
```

## 🚀 Executar Testes

### Executar todos os testes
```bash
pytest
```

### Executar com cobertura
```bash
pytest --cov=app --cov-report=html
```

### Executar testes específicos
```bash
# Apenas testes unitários
pytest -m unit

# Apenas testes de integração
pytest -m integration

# Apenas testes de autenticação
pytest -m auth

# Apenas testes de tarefas
pytest -m tasks

# Arquivo específico
pytest tests/test_auth_service.py

# Função específica
pytest tests/test_auth_service.py::TestAuthService::test_register_user_success
```

### Executar com verbosidade
```bash
pytest -v
```

## 📊 Cobertura de Código

Após executar os testes com cobertura, um relatório HTML será gerado em `htmlcov/index.html`.

Para ver a cobertura no terminal:
```bash
pytest --cov=app --cov-report=term-missing
```

## 🧪 Tipos de Testes

### Testes Unitários (`@pytest.mark.unit`)
- Testam componentes isolados (serviços, modelos)
- Não dependem de HTTP ou base de dados real
- Executam rapidamente

### Testes de Integração (`@pytest.mark.integration`)
- Testam fluxos completos (rotas HTTP)
- Usam cliente de teste Flask
- Testam interação entre componentes

## 🔧 Fixtures Disponíveis

- `app`: Instância da aplicação Flask para testes
- `client`: Cliente HTTP para fazer requisições
- `auth_headers`: Headers de autenticação JWT
- `test_user`: Utilizador de teste na base de dados
- `test_task`: Tarefa de teste na base de dados
- `another_user`: Outro utilizador de teste

## 📝 Exemplos

### Teste de Serviço
```python
def test_register_user_success(self, app):
    user_data = UserCreate(
        username='newuser',
        email='newuser@example.com',
        password='password123'
    )
    result = AuthService.register_user(user_data)
    assert result['username'] == 'newuser'
```

### Teste de Rota
```python
def test_login_success(self, client):
    login_data = {
        'username': 'testuser',
        'password': 'testpass123'
    }
    response = client.post('/api/auth/login', json=login_data)
    assert response.status_code == 200
    assert 'access_token' in response.get_json()
```

## ✅ Cobertura Atual

Os testes cobrem:
- ✅ Modelos (User, Task)
- ✅ Serviços (AuthService, TaskService)
- ✅ Rotas de autenticação (register, login)
- ✅ Rotas de tarefas (CRUD completo)
- ✅ Tratamento de erros
- ✅ Validação de dados
- ✅ Autorização e isolamento de recursos

## 🎯 Boas Práticas

1. **Isolamento**: Cada teste é independente
2. **Fixtures**: Reutilização de código comum
3. **Marcadores**: Organização por tipo de teste
4. **Nomes descritivos**: Fácil identificar o que está sendo testado
5. **Assertions claras**: Verificações específicas e legíveis

