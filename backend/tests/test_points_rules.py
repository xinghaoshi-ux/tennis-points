import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_points_rule(client: AsyncClient, auth_headers: dict):
    # Need active season
    resp = await client.post("/api/v1/admin/seasons", json={
        "name": "Rule Season", "start_date": "2026-01-01", "end_date": "2026-12-31",
    }, headers=auth_headers)
    season_id = resp.json()["data"]["id"]
    await client.post(f"/api/v1/admin/seasons/{season_id}/activate", headers=auth_headers)

    response = await client.post("/api/v1/admin/points-rules", json={
        "rule_type": "individual_event",
        "event_level": "THA500",
        "group_name": "甲组",
        "result_type": "champion",
        "points": 500,
    }, headers=auth_headers)
    assert response.status_code == 201
    data = response.json()["data"]
    assert data["points"] == 500
    assert data["rule_type"] == "individual_event"


@pytest.mark.asyncio
async def test_duplicate_rule_fails(client: AsyncClient, auth_headers: dict):
    resp = await client.post("/api/v1/admin/seasons", json={
        "name": "Dup Season", "start_date": "2026-01-01", "end_date": "2026-12-31",
    }, headers=auth_headers)
    season_id = resp.json()["data"]["id"]
    await client.post(f"/api/v1/admin/seasons/{season_id}/activate", headers=auth_headers)

    rule_data = {
        "rule_type": "individual_event",
        "event_level": "THA500",
        "group_name": "甲组",
        "result_type": "runner_up",
        "points": 300,
    }
    await client.post("/api/v1/admin/points-rules", json=rule_data, headers=auth_headers)
    response = await client.post("/api/v1/admin/points-rules", json=rule_data, headers=auth_headers)
    assert response.status_code == 409
    assert response.json()["code"] == "RULE_DUPLICATE"


@pytest.mark.asyncio
async def test_delete_rule(client: AsyncClient, auth_headers: dict):
    resp = await client.post("/api/v1/admin/seasons", json={
        "name": "Del Season", "start_date": "2026-01-01", "end_date": "2026-12-31",
    }, headers=auth_headers)
    season_id = resp.json()["data"]["id"]
    await client.post(f"/api/v1/admin/seasons/{season_id}/activate", headers=auth_headers)

    resp = await client.post("/api/v1/admin/points-rules", json={
        "rule_type": "travel_bonus", "points": 200,
    }, headers=auth_headers)
    rule_id = resp.json()["data"]["id"]

    response = await client.delete(f"/api/v1/admin/points-rules/{rule_id}", headers=auth_headers)
    assert response.status_code == 200
