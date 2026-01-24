"""
Teste simples: POST /banco/contas
"""
import pytest

'''
pytest tests2/test_banco_criar_conta.py -v
'''

@pytest.mark.asyncio
async def test_criar_conta(client):
    """Teste da rota POST /banco/contas"""
    # Primeiro cria um cliente
    await client.post("/banco/clientes/", json={
        "nome": "João Silva",
        "cpf": "12345678901",
        "endereco": "Rua das Flores, 123",
        "data_nascimento": "1990-05-15"
    })
    
    # Cria uma conta
    response = await client.post("/banco/contas/", json={
        "numero": 123456,
        "cpf": "12345678901"
    })
    assert response.status_code == 201
    assert response.json()["numero"] == 123456
