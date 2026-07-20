import pytest

pytestmark = pytest.mark.asyncio


async def test_upsert_record_creates_new(client, auth_header, seed_releases):
    body = {
        "nca_number": "test_nca_new_001",
        "nca_type": "test_type_new",
        "released_date": "2024-06-01",
        "department": "Test New Department",
        "purpose": "Test new purpose",
        "release_id": "test_release_a",
    }
    response = client.post("/private/records", json=body, headers=auth_header)
    assert response.status_code == 201
    data = response.json()
    assert data["nca_number"] == "test_nca_new_001"
    assert data["release_id"] == "test_release_a"


async def test_upsert_record_updates_existing(client, auth_header, seed_records):
    body = {
        "nca_number": "test_nca_001",
        "nca_type": "test_type_updated",
        "released_date": "2024-12-01",
        "department": "Test Updated Department",
        "purpose": "Test updated purpose",
        "release_id": "test_release_a",
    }
    response = client.post("/private/records", json=body, headers=auth_header)
    assert response.status_code == 201
    data = response.json()
    assert data["nca_number"] == "test_nca_001"
    assert data["department"] == "Test Updated Department"
    assert data["nca_type"] == "test_type_updated"

    get_resp = client.get(f"/records/{data['id']}")
    assert get_resp.status_code == 200
    assert get_resp.json()["department"] == "Test Updated Department"


async def test_upsert_record_missing_required_field(client, auth_header):
    response = client.post(
        "/private/records",
        json={"nca_number": "test_incomplete"},
        headers=auth_header,
    )
    assert response.status_code == 422


async def test_upsert_record_invalid_release_fk(client, auth_header):
    body = {
        "nca_number": "test_nca_bad_fk",
        "nca_type": "test",
        "released_date": "2024-01-01",
        "department": "Test",
        "purpose": "Test",
        "release_id": "nonexistent_release",
    }
    response = client.post("/private/records", json=body, headers=auth_header)
    assert response.status_code == 500


async def test_upsert_record_empty_body(client, auth_header):
    response = client.post(
        "/private/records",
        json={},
        headers=auth_header,
    )
    assert response.status_code == 422
