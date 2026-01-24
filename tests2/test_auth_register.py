"""
Teste simples: POST /auth/register
"""
import pytest

'''
pytest tests2/test_auth_register.py -v

'''

@pytest.mark.asyncio
async def test_register(client):
    """Teste da rota POST /auth/register"""
    response = await client.post("/auth/register", json={
        "username": "dodi",
        "password": "1234"
    })
    assert response.status_code == 200
    assert "id" in response.json()
    assert response.json()["username"] == "dodi"
