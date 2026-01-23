"""
Teste simples: GET /get/clientes
"""
import pytest


@pytest.mark.asyncio
async def test_listar_clientes(client):
    """Teste da rota GET /get/clientes"""
    # Cria um cliente
    await client.post("/banco/clientes/", json={
        "nome": "João Silva",
        "cpf": "12345678901",
        "endereco": "Rua das Flores, 123",
        "data_nascimento": "1990-05-15"
    })
    
    # Lista os clientes
    response = await client.get("/get/clientes")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) == 1
