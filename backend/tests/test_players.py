import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_player(client: AsyncClient, auth_headers: dict):
    response = await client.post("/api/v1/admin/players", json={
        "full_name": "张三",
        "gender": "male",
        "birth_date": "1988-05-12",
        "department": "计算机系",
    }, headers=auth_headers)
    assert response.status_code == 201
    data = response.json()["data"]
    assert data["full_name"] == "张三"
    assert data["status"] == "active"


@pytest.mark.asyncio
async def test_list_players_with_search(client: AsyncClient, auth_headers: dict):
    await client.post("/api/v1/admin/players", json={
        "full_name": "李四", "department": "经管学院",
    }, headers=auth_headers)
    await client.post("/api/v1/admin/players", json={
        "full_name": "王五", "department": "计算机系",
    }, headers=auth_headers)

    response = await client.get("/api/v1/admin/players?search=李", headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["total"] >= 1

    response = await client.get("/api/v1/admin/players?department=计算机系", headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["total"] >= 1


@pytest.mark.asyncio
async def test_get_player_not_found(client: AsyncClient, auth_headers: dict):
    response = await client.get("/api/v1/admin/players/99999", headers=auth_headers)
    assert response.status_code == 404
