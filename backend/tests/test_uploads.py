import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_upload_without_file(client: AsyncClient, auth_headers: dict):
    response = await client.post("/api/v1/admin/uploads", headers=auth_headers)
    assert response.status_code == 422
