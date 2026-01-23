"""
Teste simples: POST /auth/register
"""
import pytest


@pytest.mark.asyncio
async def test_register(client):
    """Teste da rota POST /auth/register"""
    response = await client.post("/auth/register", json={
        "username": "usuario_teste",
        "password": "senha123"
    })
    assert response.status_code == 200
    assert "id" in response.json()
    assert response.json()["username"] == "usuario_teste"
