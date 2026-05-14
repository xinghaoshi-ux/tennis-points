import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_public_rankings_empty(client: AsyncClient):
    response = await client.get("/api/v1/public/rankings")
    assert response.status_code == 200
    assert response.json()["data"] == []


@pytest.mark.asyncio
async def test_public_current_season_none(client: AsyncClient):
    response = await client.get("/api/v1/public/seasons/current")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_public_departments(client: AsyncClient, auth_headers: dict):
    await client.post("/api/v1/admin/players", json={
        "full_name": "Dept Test", "department": "物理系",
    }, headers=auth_headers)

    response = await client.get("/api/v1/public/departments")
    assert response.status_code == 200
    assert "物理系" in response.json()["data"]
