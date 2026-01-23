"""
Teste simples: GET /banco/contas/{conta}
"""
import pytest


@pytest.mark.asyncio
async def test_consultar_conta(client):
    """Teste da rota GET /banco/contas/{conta}"""
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
    
    # Consulta a conta
    response = await client.get("/banco/contas/123456")
    assert response.status_code == 200
    assert response.json()["numero"] == 123456
