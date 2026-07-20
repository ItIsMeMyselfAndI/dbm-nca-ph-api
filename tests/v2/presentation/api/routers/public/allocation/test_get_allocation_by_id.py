import pytest

pytestmark = pytest.mark.asyncio


async def test_get_allocation_by_id(client, seed_allocations):
    alloc_id = seed_allocations[0]["id"]
    response = client.get(f"/allocations/{alloc_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == alloc_id


async def test_get_allocation_by_id_not_found(client, seed_allocations):
    response = client.get("/allocations/00000000-0000-0000-0000-000000000000")
    assert response.status_code == 404


async def test_get_allocation_by_id_in_upper_case(client, seed_allocations):
    alloc_id = seed_allocations[0]["id"].upper()
    response = client.get(f"/allocations/{alloc_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == seed_allocations[0]["id"]


async def test_get_allocation_by_id_leading_trailing_spaces(
    client, seed_allocations
):
    alloc_id = seed_allocations[0]["id"]
    response = client.get(f"/allocations/ {alloc_id} ")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == alloc_id
