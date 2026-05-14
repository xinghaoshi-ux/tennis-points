import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import hash_password
from app.models.user import User


@pytest.mark.asyncio
async def test_login_success(client: AsyncClient, db_session: AsyncSession):
    user = User(username="logintest", password_hash=hash_password("pass123"), display_name="Test")
    db_session.add(user)
    await db_session.commit()

    response = await client.post("/api/v1/admin/auth/login", json={
        "username": "logintest",
        "password": "pass123",
    })
    assert response.status_code == 200
    data = response.json()["data"]
    assert "access_token" in data
    assert data["user"]["username"] == "logintest"


@pytest.mark.asyncio
async def test_login_invalid_credentials(client: AsyncClient):
    response = await client.post("/api/v1/admin/auth/login", json={
        "username": "nonexistent",
        "password": "wrong",
    })
    assert response.status_code == 401
    assert response.json()["code"] == "AUTH_CREDENTIALS_INVALID"


@pytest.mark.asyncio
async def test_me_without_token(client: AsyncClient):
    response = await client.get("/api/v1/admin/auth/me")
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_me_with_token(client: AsyncClient, auth_headers: dict):
    response = await client.get("/api/v1/admin/auth/me", headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["data"]["username"] == "testadmin"
