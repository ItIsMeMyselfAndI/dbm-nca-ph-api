import pytest

pytestmark = pytest.mark.asyncio


async def test_delete_record_existing(client, auth_header, seed_records):
    response = client.delete(
        "/private/records/test_nca_001", headers=auth_header
    )
    assert response.status_code == 204

    get_resp = client.get(f"/records/{seed_records[0]['id']}")
    assert get_resp.status_code == 404


async def test_delete_record_not_found(client, auth_header):
    response = client.delete(
        "/private/records/test_nca_nonexistent", headers=auth_header
    )
    assert response.status_code == 404
