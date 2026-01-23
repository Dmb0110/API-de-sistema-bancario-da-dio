"""
Teste simples: GET /get/contas
"""
import pytest


@pytest.mark.asyncio
async def test_listar_contas(client):
    """Teste da rota GET /get/contas"""
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
    
    # Lista as contas
    response = await client.get("/get/contas")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) == 1
