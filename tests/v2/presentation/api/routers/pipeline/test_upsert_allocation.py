def test_upsert_allocation_201(client):
    response = client.post(
        "/pipeline/allocations",
        json={
            "nca_number": "NCA-TEST-99-0000001",
            "agency": "Test Agency",
            "operating_unit": "Test OU",
            "amount": 50000.0,
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["nca_number"] == "NCA-TEST-99-0000001"
    assert data["agency"] == "Test Agency"
    assert data["operating_unit"] == "Test OU"
    assert data["amount"] == 50000.0
    assert "id" in data


def test_upsert_allocation_200(client):
    existing = client.get("/allocations?limit=1").json()["items"][0]

    response = client.post(
        "/pipeline/allocations",
        json={
            "nca_number": existing["nca_number"],
            "agency": existing["agency"] or "",
            "operating_unit": existing["operating_unit"] or "",
            "amount": 999999.0,
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["nca_number"] == existing["nca_number"]
    assert data["amount"] == 999999.0


def test_upsert_allocation_same_nca_diff_agency(client):
    existing = client.get("/allocations?limit=1").json()["items"][0]

    response = client.post(
        "/pipeline/allocations",
        json={
            "nca_number": existing["nca_number"],
            "agency": "Different Agency",
            "operating_unit": existing["operating_unit"] or "",
            "amount": 1000.0,
        },
    )
    assert response.status_code == 201
    assert response.json()["agency"] == "Different Agency"


def test_upsert_allocation_422_missing_fields(client):
    response = client.post("/pipeline/allocations", json={})
    assert response.status_code == 422


def test_upsert_allocation_422_missing_amount(client):
    response = client.post(
        "/pipeline/allocations",
        json={
            "nca_number": "NCA-TEST-99-0000001",
            "agency": "Agency",
            "operating_unit": "OU",
        },
    )
    assert response.status_code == 422


def test_upsert_allocation_non_numeric_amount(client):
    response = client.post(
        "/pipeline/allocations",
        json={
            "nca_number": "NCA-TEST-99-0000001",
            "agency": "Agency",
            "operating_unit": "OU",
            "amount": "not-a-number",
        },
    )
    assert response.status_code == 422
