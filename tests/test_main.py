"""
Testes do pytest para todas as rotas da API de Sistema Bancário
"""
import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, AsyncEngineType
from sqlalchemy.orm import sessionmaker
from unittest.mock import AsyncMock, patch

from app.main import app
from app.database.session import Base, get_session
from app.autenticacao_bancaria.auth import criar_token_acesso


# ================================
# Configuração do Banco de Testes
# ================================

# URL de banco de dados em memória para testes
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

# Engine e SessionLocal para testes
engine_test: AsyncEngineType = create_async_engine(
    TEST_DATABASE_URL,
    echo=False,
    connect_args={"check_same_thread": False},
)

SessionLocalTest = sessionmaker(
    bind=engine_test,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
    autocommit=False,
)


async def override_get_session() -> AsyncSession:
    """Substitui a dependência get_session para usar o banco de testes"""
    async with SessionLocalTest() as session:
        yield session


@pytest.fixture(scope="function")
async def setup_db():
    """Cria as tabelas no banco de testes"""
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # Limpa as tabelas após cada teste
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope="function")
def override_dependencies():
    """Sobrescreve a dependência de sessão"""
    app.dependency_overrides[get_session] = override_get_session


@pytest.fixture
async def client(setup_db, override_dependencies):
    """Cliente HTTP assíncrono para testes"""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


# ================================
# Fixtures de Dados de Teste
# ================================

@pytest.fixture
def usuario_teste():
    """Dados de um usuário para teste"""
    return {
        "username": "usuario_teste",
        "password": "senha123"
    }


@pytest.fixture
def usuario_teste_2():
    """Dados de um segundo usuário para teste"""
    return {
        "username": "usuario_teste_2",
        "password": "senha456"
    }


@pytest.fixture
def cliente_teste():
    """Dados de um cliente para teste"""
    return {
        "nome": "João Silva",
        "cpf": "12345678901",
        "endereco": "Rua das Flores, 123",
        "data_nascimento": "1990-05-15"
    }


@pytest.fixture
def cliente_teste_2():
    """Dados de um segundo cliente para teste"""
    return {
        "nome": "Maria Santos",
        "cpf": "98765432100",
        "endereco": "Avenida Principal, 456",
        "data_nascimento": "1995-08-20"
    }


@pytest.fixture
def conta_teste(cliente_teste):
    """Dados de uma conta para teste"""
    return {
        "numero": 123456,
        "cpf": cliente_teste["cpf"]
    }


@pytest.fixture
def conta_teste_2(cliente_teste):
    """Dados de uma segunda conta para teste"""
    return {
        "numero": 789012,
        "cpf": cliente_teste["cpf"]
    }


@pytest.fixture
def transacao_deposito(conta_teste):
    """Dados de uma transação de depósito"""
    return {
        "numero_conta": conta_teste["numero"],
        "tipo_de_transacao": "deposito",
        "valor": 1000.00
    }


@pytest.fixture
def transacao_saque(conta_teste):
    """Dados de uma transação de saque"""
    return {
        "numero_conta": conta_teste["numero"],
        "tipo_de_transacao": "saque",
        "valor": 100.00
    }


# ================================
# Testes - Autenticação (Auth)
# ================================

@pytest.mark.asyncio
async def test_register_usuario_sucesso(client, usuario_teste):
    """Testa o registro bem-sucedido de um novo usuário"""
    response = await client.post("/auth/register", json=usuario_teste)
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == usuario_teste["username"]
    assert "id" in data


@pytest.mark.asyncio
async def test_register_usuario_duplicado(client, usuario_teste):
    """Testa o registro de um usuário que já existe"""
    # Primeiro registro
    await client.post("/auth/register", json=usuario_teste)
    
    # Tentativa de registrar novamente
    response = await client.post("/auth/register", json=usuario_teste)
    assert response.status_code == 400
    assert "ja existe" in response.json()["detail"]


@pytest.mark.asyncio
async def test_login_sucesso(client, usuario_teste):
    """Testa o login bem-sucedido de um usuário"""
    # Registra o usuário primeiro
    await client.post("/auth/register", json=usuario_teste)
    
    # Realiza o login
    response = await client.post("/auth/login", json=usuario_teste)
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_login_credenciais_invalidas(client, usuario_teste):
    """Testa o login com credenciais inválidas"""
    # Registra um usuário
    await client.post("/auth/register", json=usuario_teste)
    
    # Tenta fazer login com senha incorreta
    response = await client.post("/auth/login", json={
        "username": usuario_teste["username"],
        "password": "senha_errada"
    })
    assert response.status_code == 400
    assert "invalidas" in response.json()["detail"]


@pytest.mark.asyncio
async def test_login_usuario_inexistente(client):
    """Testa o login de um usuário que não existe"""
    response = await client.post("/auth/login", json={
        "username": "usuario_inexistente",
        "password": "qualquer_senha"
    })
    assert response.status_code == 400
    assert "invalidas" in response.json()["detail"]


# ================================
# Testes - Clientes (Banco)
# ================================

@pytest.mark.asyncio
async def test_criar_cliente_sucesso(client, cliente_teste):
    """Testa a criação bem-sucedida de um cliente"""
    response = await client.post("/banco/clientes/", json=cliente_teste)
    assert response.status_code == 201
    data = response.json()
    assert data["nome"] == cliente_teste["nome"]
    assert data["cpf"] == cliente_teste["cpf"]
    assert "id" in data


@pytest.mark.asyncio
async def test_criar_cliente_cpf_duplicado(client, cliente_teste):
    """Testa a criação de um cliente com CPF duplicado"""
    # Cria o primeiro cliente
    await client.post("/banco/clientes/", json=cliente_teste)
    
    # Tenta criar outro cliente com o mesmo CPF
    response = await client.post("/banco/clientes/", json=cliente_teste)
    assert response.status_code == 400
    assert "ja existe" in response.json()["detail"]


@pytest.mark.asyncio
async def test_criar_multiplos_clientes(client, cliente_teste, cliente_teste_2):
    """Testa a criação de múltiplos clientes"""
    response1 = await client.post("/banco/clientes/", json=cliente_teste)
    response2 = await client.post("/banco/clientes/", json=cliente_teste_2)
    
    assert response1.status_code == 201
    assert response2.status_code == 201
    
    data1 = response1.json()
    data2 = response2.json()
    assert data1["id"] != data2["id"]


@pytest.mark.asyncio
async def test_listar_clientes(client, cliente_teste):
    """Testa a listagem de clientes"""
    # Cria um cliente
    await client.post("/banco/clientes/", json=cliente_teste)
    
    # Lista os clientes
    response = await client.get("/get/clientes")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["nome"] == cliente_teste["nome"]


@pytest.mark.asyncio
async def test_listar_clientes_vazio(client):
    """Testa a listagem de clientes quando não há nenhum"""
    response = await client.get("/get/clientes")
    assert response.status_code == 404
    assert "nao encontrados" in response.json()["detail"]


@pytest.mark.asyncio
async def test_consultar_cliente_por_id(client, cliente_teste):
    """Testa a consulta de um cliente específico"""
    # Cria um cliente
    create_response = await client.post("/banco/clientes/", json=cliente_teste)
    cliente_id = create_response.json()["id"]
    
    # Consulta o cliente
    response = await client.get(f"/get/cliente/{cliente_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == cliente_id
    assert data["nome"] == cliente_teste["nome"]


@pytest.mark.asyncio
async def test_consultar_cliente_inexistente(client):
    """Testa a consulta de um cliente que não existe"""
    response = await client.get("/get/cliente/999")
    assert response.status_code == 404
    assert "nao encontrado" in response.json()["detail"]


# ================================
# Testes - Contas (Banco)
# ================================

@pytest.mark.asyncio
async def test_criar_conta_sucesso(client, cliente_teste, conta_teste):
    """Testa a criação bem-sucedida de uma conta"""
    # Cria um cliente primeiro
    await client.post("/banco/clientes/", json=cliente_teste)
    
    # Cria uma conta
    response = await client.post("/banco/contas/", json=conta_teste)
    assert response.status_code == 201
    data = response.json()
    assert data["numero"] == conta_teste["numero"]
    assert "saldo" in data


@pytest.mark.asyncio
async def test_criar_conta_cliente_inexistente(client, conta_teste):
    """Testa a criação de uma conta para um cliente inexistente"""
    response = await client.post("/banco/contas/", json=conta_teste)
    assert response.status_code == 404
    assert "nao encontrado" in response.json()["detail"]


@pytest.mark.asyncio
async def test_criar_conta_numero_duplicado(client, cliente_teste, conta_teste):
    """Testa a criação de uma conta com número duplicado"""
    # Cria um cliente
    await client.post("/banco/clientes/", json=cliente_teste)
    
    # Cria a primeira conta
    await client.post("/banco/contas/", json=conta_teste)
    
    # Tenta criar outra conta com o mesmo número
    response = await client.post("/banco/contas/", json=conta_teste)
    assert response.status_code == 400
    assert "ja existe" in response.json()["detail"]


@pytest.mark.asyncio
async def test_consultar_conta_sucesso(client, cliente_teste, conta_teste):
    """Testa a consulta bem-sucedida de uma conta"""
    # Cria um cliente e uma conta
    await client.post("/banco/clientes/", json=cliente_teste)
    await client.post("/banco/contas/", json=conta_teste)
    
    # Consulta a conta
    response = await client.get(f"/banco/contas/{conta_teste['numero']}")
    assert response.status_code == 200
    data = response.json()
    assert data["numero"] == conta_teste["numero"]
    assert "saldo" in data


@pytest.mark.asyncio
async def test_consultar_conta_inexistente(client):
    """Testa a consulta de uma conta que não existe"""
    response = await client.get("/banco/contas/999999")
    assert response.status_code == 404
    assert "nao encontrada" in response.json()["detail"]


@pytest.mark.asyncio
async def test_listar_contas(client, cliente_teste, conta_teste):
    """Testa a listagem de contas"""
    # Cria um cliente e uma conta
    await client.post("/banco/clientes/", json=cliente_teste)
    await client.post("/banco/contas/", json=conta_teste)
    
    # Lista as contas
    response = await client.get("/get/contas")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 1


@pytest.mark.asyncio
async def test_listar_contas_vazio(client):
    """Testa a listagem de contas quando não há nenhuma"""
    response = await client.get("/get/contas")
    assert response.status_code == 404
    assert "nao encontradas" in response.json()["detail"]


# ================================
# Testes - Transações (Banco)
# ================================

@pytest.mark.asyncio
async def test_criar_transacao_deposito_sucesso(client, usuario_teste, cliente_teste, conta_teste, transacao_deposito):
    """Testa a realização bem-sucedida de um depósito"""
    # Registra e faz login
    await client.post("/auth/register", json=usuario_teste)
    login_response = await client.post("/auth/login", json=usuario_teste)
    token = login_response.json()["access_token"]
    
    # Cria cliente e conta
    await client.post("/banco/clientes/", json=cliente_teste)
    await client.post("/banco/contas/", json=conta_teste)
    
    # Realiza o depósito
    response = await client.post(
        "/banco/transacoes/",
        json=transacao_deposito,
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "mensagem" in data


@pytest.mark.asyncio
async def test_criar_transacao_saque_sucesso(client, usuario_teste, cliente_teste, conta_teste, transacao_deposito, transacao_saque):
    """Testa a realização bem-sucedida de um saque"""
    # Registra e faz login
    await client.post("/auth/register", json=usuario_teste)
    login_response = await client.post("/auth/login", json=usuario_teste)
    token = login_response.json()["access_token"]
    
    # Cria cliente e conta
    await client.post("/banco/clientes/", json=cliente_teste)
    await client.post("/banco/contas/", json=conta_teste)
    
    # Realiza um depósito primeiro
    await client.post(
        "/banco/transacoes/",
        json=transacao_deposito,
        headers={"Authorization": f"Bearer {token}"}
    )
    
    # Realiza o saque
    response = await client.post(
        "/banco/transacoes/",
        json=transacao_saque,
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "mensagem" in data


@pytest.mark.asyncio
async def test_criar_transacao_saque_saldo_insuficiente(client, usuario_teste, cliente_teste, conta_teste, transacao_saque):
    """Testa um saque com saldo insuficiente"""
    # Registra e faz login
    await client.post("/auth/register", json=usuario_teste)
    login_response = await client.post("/auth/login", json=usuario_teste)
    token = login_response.json()["access_token"]
    
    # Cria cliente e conta
    await client.post("/banco/clientes/", json=cliente_teste)
    await client.post("/banco/contas/", json=conta_teste)
    
    # Tenta fazer um saque sem saldo
    response = await client.post(
        "/banco/transacoes/",
        json=transacao_saque,
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 400
    assert "saldo insuficiente" in response.json()["detail"].lower()


@pytest.mark.asyncio
async def test_criar_transacao_tipo_invalido(client, usuario_teste, cliente_teste, conta_teste):
    """Testa uma transação com tipo inválido"""
    # Registra e faz login
    await client.post("/auth/register", json=usuario_teste)
    login_response = await client.post("/auth/login", json=usuario_teste)
    token = login_response.json()["access_token"]
    
    # Cria cliente e conta
    await client.post("/banco/clientes/", json=cliente_teste)
    await client.post("/banco/contas/", json=conta_teste)
    
    # Tenta fazer uma transação com tipo inválido
    response = await client.post(
        "/banco/transacoes/",
        json={
            "numero_conta": conta_teste["numero"],
            "tipo_de_transacao": "transferencia",
            "valor": 100.00
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 400
    assert "invalido" in response.json()["detail"].lower()


@pytest.mark.asyncio
async def test_criar_transacao_conta_inexistente(client, usuario_teste, transacao_saque):
    """Testa uma transação para uma conta inexistente"""
    # Registra e faz login
    await client.post("/auth/register", json=usuario_teste)
    login_response = await client.post("/auth/login", json=usuario_teste)
    token = login_response.json()["access_token"]
    
    # Tenta fazer uma transação sem a conta existir
    response = await client.post(
        "/banco/transacoes/",
        json=transacao_saque,
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 404
    assert "nao encontrada" in response.json()["detail"]


@pytest.mark.asyncio
async def test_criar_transacao_sem_autenticacao(client, cliente_teste, conta_teste, transacao_deposito):
    """Testa uma transação sem estar autenticado"""
    # Cria cliente e conta sem autenticação
    await client.post("/banco/clientes/", json=cliente_teste)
    await client.post("/banco/contas/", json=conta_teste)
    
    # Tenta fazer uma transação sem token
    response = await client.post(
        "/banco/transacoes/",
        json=transacao_deposito
    )
    assert response.status_code == 403


# ================================
# Testes - Rota Protegida
# ================================

@pytest.mark.asyncio
async def test_protected_route_com_autenticacao(client, usuario_teste):
    """Testa acesso a rota protegida com autenticação"""
    # Registra e faz login
    await client.post("/auth/register", json=usuario_teste)
    login_response = await client.post("/auth/login", json=usuario_teste)
    token = login_response.json()["access_token"]
    
    # Acessa a rota protegida
    response = await client.get(
        "/banco/protected",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert "Bem-vindo" in response.json()["msg"]


@pytest.mark.asyncio
async def test_protected_route_sem_autenticacao(client):
    """Testa acesso a rota protegida sem autenticação"""
    response = await client.get("/banco/protected")
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_protected_route_token_invalido(client):
    """Testa acesso a rota protegida com token inválido"""
    response = await client.get(
        "/banco/protected",
        headers={"Authorization": "Bearer token_invalido"}
    )
    assert response.status_code == 403


# ================================
# Testes - Fluxo Completo
# ================================

@pytest.mark.asyncio
async def test_fluxo_completo_banco(client, usuario_teste, cliente_teste, conta_teste):
    """Testa um fluxo completo de operações bancárias"""
    # 1. Registra um novo usuário
    register_response = await client.post("/auth/register", json=usuario_teste)
    assert register_response.status_code == 200
    
    # 2. Faz login
    login_response = await client.post("/auth/login", json=usuario_teste)
    assert login_response.status_code == 200
    token = login_response.json()["access_token"]
    
    # 3. Cria um cliente
    cliente_response = await client.post("/banco/clientes/", json=cliente_teste)
    assert cliente_response.status_code == 201
    cliente_id = cliente_response.json()["id"]
    
    # 4. Cria uma conta
    conta_response = await client.post("/banco/contas/", json=conta_teste)
    assert conta_response.status_code == 201
    
    # 5. Realiza um depósito
    deposito_response = await client.post(
        "/banco/transacoes/",
        json={
            "numero_conta": conta_teste["numero"],
            "tipo_de_transacao": "deposito",
            "valor": 5000.00
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    assert deposito_response.status_code == 200
    
    # 6. Consulta a conta
    consulta_response = await client.get(f"/banco/contas/{conta_teste['numero']}")
    assert consulta_response.status_code == 200
    assert consulta_response.json()["saldo"] == 5000.00
    
    # 7. Realiza um saque
    saque_response = await client.post(
        "/banco/transacoes/",
        json={
            "numero_conta": conta_teste["numero"],
            "tipo_de_transacao": "saque",
            "valor": 1000.00
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    assert saque_response.status_code == 200
    
    # 8. Consulta a conta novamente
    consulta_final = await client.get(f"/banco/contas/{conta_teste['numero']}")
    assert consulta_final.status_code == 200
    assert consulta_final.json()["saldo"] == 4000.00
    
    # 9. Lista os clientes
    lista_response = await client.get("/get/clientes")
    assert lista_response.status_code == 200
    assert len(lista_response.json()) == 1


# ================================
# Testes - Validações de Dados
# ================================

@pytest.mark.asyncio
async def test_criar_cliente_campos_obrigatorios(client):
    """Testa a validação de campos obrigatórios ao criar cliente"""
    # Tenta criar um cliente sem CPF
    response = await client.post("/banco/clientes/", json={
        "nome": "João Silva",
        "endereco": "Rua das Flores, 123",
        "data_nascimento": "1990-05-15"
    })
    assert response.status_code == 422  # Unprocessable Entity


@pytest.mark.asyncio
async def test_criar_conta_campos_obrigatorios(client):
    """Testa a validação de campos obrigatórios ao criar conta"""
    # Tenta criar uma conta sem número
    response = await client.post("/banco/contas/", json={
        "cpf": "12345678901"
    })
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_transacao_valor_negativo(client, usuario_teste, cliente_teste, conta_teste):
    """Testa uma transação com valor negativo"""
    # Registra e faz login
    await client.post("/auth/register", json=usuario_teste)
    login_response = await client.post("/auth/login", json=usuario_teste)
    token = login_response.json()["access_token"]
    
    # Cria cliente e conta
    await client.post("/banco/clientes/", json=cliente_teste)
    await client.post("/banco/contas/", json=conta_teste)
    
    # Tenta fazer uma transação com valor negativo
    response = await client.post(
        "/banco/transacoes/",
        json={
            "numero_conta": conta_teste["numero"],
            "tipo_de_transacao": "deposito",
            "valor": -100.00
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    # Pode retornar 422 (validação) ou processar dependendo da lógica do serviço
    assert response.status_code in [400, 422]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
