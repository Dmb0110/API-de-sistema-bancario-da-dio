"""
Teste simples: GET /get/cliente/{cliente_id}
"""
import pytest


@pytest.mark.asyncio
async def test_consultar_cliente(client):
    """Teste da rota GET /get/cliente/{cliente_id}"""
    # Cria um cliente
    create = await client.post("/banco/clientes/", json={
        "nome": "João Silva",
        "cpf": "12345678901",
        "endereco": "Rua das Flores, 123",
        "data_nascimento": "1990-05-15"
    })
    cliente_id = create.json()["id"]
    
    # Consulta o cliente
    response = await client.get(f"/get/cliente/{cliente_id}")
    assert response.status_code == 200
    assert response.json()["id"] == cliente_id
    assert response.json()["nome"] == "João Silva"
