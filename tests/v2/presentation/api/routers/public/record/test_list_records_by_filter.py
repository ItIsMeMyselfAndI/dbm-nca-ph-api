import pytest

pytestmark = pytest.mark.asyncio


async def test_list_records_by_department(client, seed_records):
    response = client.get("/records/department/Test Department Alpha")
    assert response.status_code == 200
    data = response.json()
    assert data["count"] == 2
    assert len(data["items"]) == 2


async def test_list_records_by_nca_type(client, seed_records):
    response = client.get("/records/nca_type/test_type_a")
    assert response.status_code == 200
    data = response.json()
    assert data["count"] == 2
    assert len(data["items"]) == 2


async def test_list_records_by_release_id(client, seed_records):
    response = client.get("/records/release_id/test_release_a")
    assert response.status_code == 200
    data = response.json()
    assert data["count"] == 3
    assert len(data["items"]) == 3


async def test_list_records_by_released_date(client, seed_records):
    response = client.get("/records/released_date/2024-01-15")
    assert response.status_code == 200
    data = response.json()
    assert data["count"] == 1
    assert len(data["items"]) == 1


async def test_list_records_by_filter_no_match(client, seed_records):
    response = client.get("/records/department/Nonexistent Department")
    assert response.status_code == 200
    data = response.json()
    assert data["count"] == 0
    assert data["next_cursor"] is None


async def test_list_records_by_filter_invalid_key(client, seed_records):
    response = client.get("/records/invalid_key/value")
    assert response.status_code == 422


async def test_list_records_by_filter_with_cursor(client, seed_records):
    response = client.get(
        "/records/release_id/test_release_a?limit=2"
    )
    assert response.status_code == 200
    data = response.json()
    assert data["count"] == 2
    assert data["next_cursor"] is not None

    response_next = client.get(
        f"/records/release_id/test_release_a?limit=2&cursor={data['next_cursor']}"
    )
    assert response_next.status_code == 200
    data_next = response_next.json()
    assert data_next["count"] == 1
