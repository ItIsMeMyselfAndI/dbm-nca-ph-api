import pytest

pytestmark = pytest.mark.asyncio


async def test_delete_release_existing(client, auth_header, seed_releases):
    response = client.delete("/private/releases/test_release_a", headers=auth_header)
    assert response.status_code == 204

    get_resp = client.get("/releases/test_release_a")
    assert get_resp.status_code == 404


async def test_delete_release_not_found(client, auth_header):
    response = client.delete(
        "/private/releases/nonexistent-id", headers=auth_header
    )
    assert response.status_code == 404
