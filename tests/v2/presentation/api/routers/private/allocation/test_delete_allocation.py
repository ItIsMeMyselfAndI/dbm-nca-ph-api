import pytest

pytestmark = pytest.mark.asyncio


async def test_delete_allocation_existing(client, auth_header, seed_allocations):
    alloc_id = seed_allocations[0]["id"]
    response = client.delete(
        f"/private/allocations/{alloc_id}", headers=auth_header
    )
    assert response.status_code == 204

    get_resp = client.get(f"/allocations/{alloc_id}")
    assert get_resp.status_code == 404


async def test_delete_allocation_not_found(client, auth_header):
    response = client.delete(
        "/private/allocations/00000000-0000-0000-0000-000000000099",
        headers=auth_header,
    )
    assert response.status_code == 404
