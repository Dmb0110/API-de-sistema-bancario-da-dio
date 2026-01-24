"""
Teste simples: POST /auth/login
"""
import pytest

'''
pytest tests2/test_auth_login.py -v

'''

@pytest.mark.asyncio
async def test_login(client):
    """Teste da rota POST /auth/login"""
    # Primeiro registra o usuário
    await client.post("/auth/register", json={
        "username": "dodi",
        "password": "1234"
    })
    
    # Faz login
    response = await client.post("/auth/login", json={
        "username": "dodi",
        "password": "1234"
    })
    
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"
