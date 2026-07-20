import pytest

pytestmark = pytest.mark.asyncio


async def test_upsert_release_creates_new(client, auth_header):
    body = {
        "id": "test_upsert_new_release",
        "title": "New Test Release",
        "url": "http://test.example/new",
        "filename": "test_new.pdf",
        "year": 2024,
        "page_count": 15,
    }
    response = client.post("/private/releases", json=body, headers=auth_header)
    assert response.status_code == 201
    data = response.json()
    assert data["id"] == "test_upsert_new_release"
    assert data["title"] == "New Test Release"
    assert data["year"] == 2024


async def test_upsert_release_updates_existing(client, auth_header, seed_releases):
    body = {
        "id": "test_release_a",
        "title": "Updated Test Release A",
        "url": "http://test.example/updated",
        "filename": "test_updated.pdf",
        "year": 2025,
        "page_count": 99,
    }
    response = client.post("/private/releases", json=body, headers=auth_header)
    assert response.status_code == 201
    data = response.json()
    assert data["id"] == "test_release_a"
    assert data["title"] == "Updated Test Release A"
    assert data["year"] == 2025

    get_resp = client.get("/releases/test_release_a")
    assert get_resp.status_code == 200
    assert get_resp.json()["url"] == "http://test.example/updated"


async def test_upsert_release_missing_required_field(client, auth_header):
    response = client.post(
        "/private/releases",
        json={"title": "Missing ID"},
        headers=auth_header,
    )
    assert response.status_code == 422


async def test_upsert_release_invalid_type(client, auth_header):
    response = client.post(
        "/private/releases",
        json={
            "id": "test_invalid",
            "title": "Invalid",
            "url": "http://test.example",
            "filename": "test.pdf",
            "year": "not-a-number",
        },
        headers=auth_header,
    )
    assert response.status_code == 422


async def test_upsert_release_empty_body(client, auth_header):
    response = client.post(
        "/private/releases",
        json={},
        headers=auth_header,
    )
    assert response.status_code == 422
