import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_season(client: AsyncClient, auth_headers: dict):
    response = await client.post("/api/v1/admin/seasons", json={
        "name": "Test Season",
        "start_date": "2026-04-01",
        "end_date": "2027-04-01",
    }, headers=auth_headers)
    assert response.status_code == 201
    data = response.json()["data"]
    assert data["name"] == "Test Season"
    assert data["status"] == "draft"


@pytest.mark.asyncio
async def test_list_seasons(client: AsyncClient, auth_headers: dict):
    await client.post("/api/v1/admin/seasons", json={
        "name": "S1", "start_date": "2026-01-01", "end_date": "2026-12-31",
    }, headers=auth_headers)

    response = await client.get("/api/v1/admin/seasons", headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["total"] >= 1


@pytest.mark.asyncio
async def test_activate_season(client: AsyncClient, auth_headers: dict):
    resp = await client.post("/api/v1/admin/seasons", json={
        "name": "Activate Test", "start_date": "2026-01-01", "end_date": "2026-12-31",
    }, headers=auth_headers)
    season_id = resp.json()["data"]["id"]

    response = await client.post(f"/api/v1/admin/seasons/{season_id}/activate", headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["data"]["status"] == "active"


@pytest.mark.asyncio
async def test_activate_non_draft_fails(client: AsyncClient, auth_headers: dict):
    resp = await client.post("/api/v1/admin/seasons", json={
        "name": "Active Test", "start_date": "2026-01-01", "end_date": "2026-12-31",
    }, headers=auth_headers)
    season_id = resp.json()["data"]["id"]
    await client.post(f"/api/v1/admin/seasons/{season_id}/activate", headers=auth_headers)

    response = await client.post(f"/api/v1/admin/seasons/{season_id}/activate", headers=auth_headers)
    assert response.status_code == 409
