import pytest

pytestmark = pytest.mark.asyncio

RELEASE_BODY = {
    "id": "test_auth_release",
    "title": "Test Auth Release",
    "url": "http://test.example/auth",
    "filename": "test_auth.pdf",
    "year": 2024,
}


async def test_private_endpoint_missing_api_key_returns_401(client):
    response = client.post("/private/releases", json=RELEASE_BODY)
    assert response.status_code == 401


async def test_private_endpoint_invalid_api_key_returns_401(client):
    response = client.post(
        "/private/releases",
        json=RELEASE_BODY,
        headers={"X-API-Key": "wrong-key"},
    )
    assert response.status_code == 401


async def test_private_endpoint_empty_api_key_returns_401(client):
    response = client.post(
        "/private/releases",
        json=RELEASE_BODY,
        headers={"X-API-Key": ""},
    )
    assert response.status_code == 401


async def test_private_delete_missing_api_key_returns_401(client):
    response = client.delete("/private/releases/some-id")
    assert response.status_code == 401
