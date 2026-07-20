import pytest

pytestmark = pytest.mark.asyncio


async def test_get_record_by_id(client, seed_records):
    record_id = seed_records[0]["id"]
    response = client.get(f"/records/{record_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == record_id
    assert data["nca_number"] == "test_nca_001"


async def test_get_record_by_id_not_found(client, seed_records):
    response = client.get("/records/00000000-0000-0000-0000-000000000000")
    assert response.status_code == 404


async def test_get_record_by_id_in_upper_case(client, seed_records):
    record_id = seed_records[0]["id"].upper()
    response = client.get(f"/records/{record_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == seed_records[0]["id"]


async def test_get_record_by_id_leading_trailing_spaces(client, seed_records):
    record_id = seed_records[0]["id"]
    response = client.get(f"/records/ {record_id} ")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == record_id
