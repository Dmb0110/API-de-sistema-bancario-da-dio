# Testes do Projeto - API de Sistema Bancário

## 📋 Visão Geral

Este projeto contém testes abrangentes usando **pytest** para todas as rotas da API de Sistema Bancário. Os testes cobrem:

- ✅ Autenticação (Registro e Login)
- ✅ Gerenciamento de Clientes
- ✅ Gerenciamento de Contas
- ✅ Transações Bancárias (Depósitos e Saques)
- ✅ Rotas Protegidas
- ✅ Validações de Dados
- ✅ Fluxos Completos de Operações

## 🛠️ Instalação das Dependências

### Pré-requisitos
- Python 3.8+
- pip ou conda

### Instalação

1. **Instale as dependências do projeto:**

```bash
pip install -r requirements.txt
```

As dependências incluem:
- `pytest` - Framework de testes
- `pytest-asyncio` - Suporte para testes assíncronos
- `httpx` - Cliente HTTP assíncrono para testes
- `aiosqlite` - Driver SQLite assíncrono para testes em memória

## 🚀 Executando os Testes

### Executar todos os testes:

```bash
pytest
```

### Executar testes com verbosidade:

```bash
pytest -v
```

### Executar um arquivo de teste específico:

```bash
pytest test_main.py
```

### Executar um teste específico:

```bash
pytest test_main.py::test_register_usuario_sucesso -v
```

### Executar testes com coverage (cobertura):

```bash
pip install pytest-cov
pytest --cov=app --cov-report=html
```

### Executar apenas testes de integração:

```bash
pytest -v -m integration
```

## 📊 Estrutura dos Testes

O arquivo `test_main.py` contém os seguintes grupos de testes:

### 1. **Testes de Autenticação** (5 testes)
- Registro de novo usuário
- Tentativa de registro duplicado
- Login bem-sucedido
- Login com credenciais inválidas
- Login de usuário inexistente

### 2. **Testes de Clientes** (6 testes)
- Criar cliente com sucesso
- CPF duplicado
- Criar múltiplos clientes
- Listar clientes
- Listar clientes vazio
- Consultar cliente por ID

### 3. **Testes de Contas** (7 testes)
- Criar conta com sucesso
- Criar conta para cliente inexistente
- Número de conta duplicado
- Consultar conta existente
- Consultar conta inexistente
- Listar contas
- Listar contas vazio

### 4. **Testes de Transações** (7 testes)
- Depósito bem-sucedido
- Saque bem-sucedido
- Saque com saldo insuficiente
- Transação com tipo inválido
- Transação em conta inexistente
- Transação sem autenticação

### 5. **Testes de Rotas Protegidas** (3 testes)
- Acesso com autenticação
- Acesso sem autenticação
- Acesso com token inválido

### 6. **Testes de Fluxo Completo** (1 teste)
- Fluxo bancário completo (registro → login → criar cliente → criar conta → depositar → sacar)

### 7. **Testes de Validações** (3 testes)
- Validação de campos obrigatórios
- Valor negativo em transação

## 🔧 Configuração do Teste

### Banco de Dados de Teste

Os testes usam um banco de dados **SQLite em memória** (`sqlite+aiosqlite:///:memory:`) para isolamento e rapidez.

### Fixtures Disponíveis

- `client` - Cliente HTTP assíncrono
- `setup_db` - Setup e teardown do banco de testes
- `usuario_teste` - Dados de usuário para testes
- `cliente_teste` - Dados de cliente para testes
- `conta_teste` - Dados de conta para testes
- `transacao_deposito` - Dados de transação de depósito
- `transacao_saque` - Dados de transação de saque

## 📝 Exemplo de Uso de Fixtures

```python
@pytest.mark.asyncio
async def test_exemplo(client, usuario_teste, cliente_teste):
    """Exemplo de teste usando fixtures"""
    response = await client.post("/auth/register", json=usuario_teste)
    assert response.status_code == 200
```

## 🐛 Troubleshooting

### Erro: "RuntimeError: Event loop is closed"
**Solução:** Certifique-se de que tem `pytest-asyncio` instalado:
```bash
pip install pytest-asyncio
```

### Erro: "ModuleNotFoundError: No module named 'app'"
**Solução:** Execute os testes a partir do diretório raiz do projeto.

### Os testes não encontram o banco de dados
**Solução:** Os testes usam SQLite em memória por padrão, então não é necessário banco externo.

## 📊 Cobertura de Testes

Para gerar um relatório de cobertura:

```bash
pytest --cov=app --cov-report=html
```

Abra `htmlcov/index.html` no navegador para ver o relatório.

## 🔐 Segurança

- Os testes usam dados de teste isolados
- Cada teste cria seu próprio banco de dados em memória
- As transações são limpas automaticamente após cada teste

## 📚 Referências

- [Pytest Documentation](https://docs.pytest.org/)
- [FastAPI Testing](https://fastapi.tiangolo.com/advanced/testing/)
- [SQLAlchemy Async](https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html)
- [Pytest-asyncio](https://pytest-asyncio.readthedocs.io/)

## 🤝 Contribuindo

Ao adicionar novas rotas, lembre-se de:
1. Adicionar testes correspondentes em `test_main.py`
2. Incluir testes de sucesso e erro
3. Usar as fixtures disponíveis
4. Manter a nomenclatura consistente

## 📄 Licença

Este projeto faz parte do exercício DIO.
