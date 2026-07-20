import pytest

pytestmark = pytest.mark.asyncio


async def test_list_allocations_by_agency(client, seed_allocations):
    response = client.get("/allocations/agency/Test Agency One")
    assert response.status_code == 200
    data = response.json()
    assert data["count"] == 2
    assert len(data["items"]) == 2


async def test_list_allocations_by_nca_number(client, seed_allocations):
    response = client.get("/allocations/nca_number/test_nca_001")
    assert response.status_code == 200
    data = response.json()
    assert data["count"] == 2
    assert len(data["items"]) == 2


async def test_list_allocations_by_operating_unit(client, seed_allocations):
    response = client.get("/allocations/operating_unit/Test OU North")
    assert response.status_code == 200
    data = response.json()
    assert data["count"] == 1
    assert len(data["items"]) == 1


async def test_list_allocations_by_filter_no_match(client, seed_allocations):
    response = client.get("/allocations/agency/Nonexistent Agency")
    assert response.status_code == 200
    data = response.json()
    assert data["count"] == 0
    assert data["next_cursor"] is None


async def test_list_allocations_by_filter_invalid_key(client, seed_allocations):
    response = client.get("/allocations/invalid_key/value")
    assert response.status_code == 422


async def test_list_allocations_by_filter_with_cursor(client, seed_allocations):
    response = client.get(
        "/allocations/agency/Test Agency One?limit=1"
    )
    assert response.status_code == 200
    data = response.json()
    assert data["count"] == 1
    assert data["next_cursor"] is not None

    response_next = client.get(
        f"/allocations/agency/Test Agency One?limit=1&cursor={data['next_cursor']}"
    )
    assert response_next.status_code == 200
    data_next = response_next.json()
    assert data_next["count"] == 1
