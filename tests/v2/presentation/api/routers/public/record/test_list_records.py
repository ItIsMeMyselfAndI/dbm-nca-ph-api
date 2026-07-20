import pytest

pytestmark = pytest.mark.asyncio


async def test_list_records(client, seed_records):
    response = client.get("/records?limit=10")
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert data["count"] == 3
    assert data["cursor"] is None


async def test_list_records_with_cursor(client, seed_records):
    response = client.get("/records?limit=2")
    assert response.status_code == 200
    data = response.json()
    assert data["count"] == 2
    assert data["next_cursor"] is not None

    response_next = client.get(f"/records?limit=2&cursor={data['next_cursor']}")
    assert response_next.status_code == 200
    data_next = response_next.json()
    assert data_next["count"] == 1


async def test_list_records_with_invalid_cursor(client, seed_records):
    response = client.get("/records?limit=2&cursor=00000000-0000-0000-0000-000000000000")
    assert response.status_code == 200
    data = response.json()
    assert data["count"] == 2
    assert data["cursor"] == "00000000-0000-0000-0000-000000000000"


async def test_list_records_with_empty_cursor(client, seed_records):
    response = client.get("/records?limit=2&cursor=")
    assert response.status_code == 400


async def test_list_records_with_limit_zero(client, seed_records):
    response = client.get("/records?limit=0")
    assert response.status_code == 200
    data = response.json()
    assert data["count"] == 0
    assert data["cursor"] is None
    assert data["next_cursor"] is None


async def test_list_records_with_negative_limit(client, seed_records):
    response = client.get("/records?limit=-5")
    assert response.status_code == 200
    data = response.json()
    assert data["count"] == 0
    assert data["cursor"] is None
    assert data["next_cursor"] is None


async def test_list_records_with_leading_trailing_spaces_cursor(
    client, seed_records
):
    first_id = seed_records[0]["id"]
    response = client.get(f"/records?limit=2&cursor= {first_id} ")
    assert response.status_code == 200
    data = response.json()
    assert data["count"] == 2
    assert data["cursor"] is not None
    assert data["next_cursor"] is not None


async def test_list_records_with_upper_case_cursor(client, seed_records):
    first_id = seed_records[0]["id"].upper()
    response = client.get(f"/records?limit=2&cursor={first_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["count"] == 2
    assert data["cursor"] is not None
    assert data["next_cursor"] is not None


async def test_list_records_with_limit_exceeding_total(client, seed_records):
    response = client.get("/records?limit=10")
    assert response.status_code == 200
    data = response.json()
    assert data["count"] == 3
    assert data["cursor"] is None
