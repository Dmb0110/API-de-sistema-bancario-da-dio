"""
Teste simples: POST /banco/clientes
"""
import pytest

'''
pytest tests2/test_banco_criar_cliente.py -v
'''

@pytest.mark.asyncio
async def test_criar_cliente(client):
    """Teste da rota POST /banco/clientes"""
    response = await client.post("/banco/clientes/", json={
        "nome": "João Silva",
        "cpf": "12345678901",
        "endereco": "Rua das Flores, 123",
        "data_nascimento": "1990-05-15"
    })
    assert response.status_code == 201
    assert response.json()["nome"] == "João Silva"
    assert response.json()["cpf"] == "12345678901"
