"""
Teste simples: GET /banco/protected
"""
import pytest


@pytest.mark.asyncio
async def test_rota_protegida(client):
    """Teste da rota GET /banco/protected"""
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
    
    # Acessa rota protegida
    response = await client.get(
        "/banco/protected",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert "Bem-vindo" in response.json()["msg"]
