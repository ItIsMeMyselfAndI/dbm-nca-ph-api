import pytest

pytestmark = pytest.mark.asyncio


async def test_upsert_allocation_creates_new(client, auth_header, seed_records):
    body = {
        "nca_number": "test_nca_001",
        "agency": "Test New Agency",
        "operating_unit": "Test New OU",
        "amount": 500000.00,
    }
    response = client.post("/private/allocations", json=body, headers=auth_header)
    assert response.status_code == 201
    data = response.json()
    assert data["nca_number"] == "test_nca_001"
    assert data["agency"] == "Test New Agency"
    assert data["operating_unit"] == "Test New OU"
    assert data["amount"] == 500000.00


async def test_upsert_allocation_updates_existing_composite_key(
    client, auth_header, seed_allocations
):
    body = {
        "nca_number": "test_nca_001",
        "agency": "Test Agency One",
        "operating_unit": "Test OU North",
        "amount": 999999.00,
    }
    response = client.post("/private/allocations", json=body, headers=auth_header)
    assert response.status_code == 201
    data = response.json()
    assert data["nca_number"] == "test_nca_001"
    assert data["agency"] == "Test Agency One"
    assert data["operating_unit"] == "Test OU North"
    assert data["amount"] == 999999.00


async def test_upsert_allocation_same_nca_different_agency_creates(
    client, auth_header, seed_allocations
):
    body = {
        "nca_number": "test_nca_001",
        "agency": "Test Brand New Agency",
        "operating_unit": "Test OU North",
        "amount": 100.00,
    }
    response = client.post("/private/allocations", json=body, headers=auth_header)
    assert response.status_code == 201
    data = response.json()
    assert data["agency"] == "Test Brand New Agency"


async def test_upsert_allocation_missing_required_field(client, auth_header):
    response = client.post(
        "/private/allocations",
        json={"nca_number": "test_incomplete"},
        headers=auth_header,
    )
    assert response.status_code == 422


async def test_upsert_allocation_empty_body(client, auth_header):
    response = client.post(
        "/private/allocations",
        json={},
        headers=auth_header,
    )
    assert response.status_code == 422


async def test_upsert_allocation_invalid_record_fk(client, auth_header):
    body = {
        "nca_number": "nonexistent_nca",
        "agency": "Test Agency",
        "operating_unit": "Test OU",
        "amount": 1000.00,
    }
    response = client.post("/private/allocations", json=body, headers=auth_header)
    assert response.status_code == 500
