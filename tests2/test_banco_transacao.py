"""
Teste simples: POST /banco/transacoes
"""
import pytest

'''
pytest tests2/test_banco_transacao.py -v
'''
@pytest.mark.asyncio
async def test_criar_transacao(client):
    """Teste da rota POST /banco/transacoes"""
    # Registra e faz login
    await client.post("/auth/register", json={
        "username": "usuario_teste",
        "password": "senha123"
    })
    login = await client.post("/auth/login", json={
        "username": "usuario_teste",
        "password": "senha123"
    })
    token = login.json()["access_token"]
    
    # Cria cliente e conta
    await client.post("/banco/clientes/", json={
        "nome": "João Silva",
        "cpf": "12345678901",
        "endereco": "Rua das Flores, 123",
        "data_nascimento": "1990-05-15"
    })
    
    await client.post("/banco/contas/", json={
        "numero": 123456,
        "cpf": "12345678901"
    })
    
    # Cria uma transação
    response = await client.post(
        "/banco/transacoes/",
        json={
            "numero_conta": 123456,
            "tipo_de_transacao": "deposito",
            "valor": 1000.00
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert "mensagem" in response.json()
