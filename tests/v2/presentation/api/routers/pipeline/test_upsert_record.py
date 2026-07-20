def test_upsert_record_201(client):
    response = client.post(
        "/pipeline/records",
        json={
            "nca_number": "NCA-TEST-99-0000001",
            "nca_type": "REG",
            "released_date": "2024-01-01T00:00:00+00:00",
            "department": "Test Department",
            "purpose": "Test purpose",
            "release_id": "id_2024",
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["nca_number"] == "NCA-TEST-99-0000001"
    assert data["nca_type"] == "REG"
    assert data["department"] == "Test Department"
    assert data["release_id"] == "id_2024"
    assert "id" in data


def test_upsert_record_200(client):
    existing_nca = client.get("/records?limit=1").json()["items"][0]["nca_number"]

    response = client.post(
        "/pipeline/records",
        json={
            "nca_number": existing_nca,
            "nca_type": "REG",
            "released_date": "2025-06-06T00:00:00+00:00",
            "department": "Updated Department",
            "purpose": "Updated purpose",
            "release_id": "id_2025",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["nca_number"] == existing_nca
    assert data["department"] == "Updated Department"


def test_upsert_record_422_missing_fields(client):
    response = client.post("/pipeline/records", json={})
    assert response.status_code == 422


def test_upsert_record_422_missing_nca_number(client):
    response = client.post(
        "/pipeline/records",
        json={
            "nca_type": "REG",
            "released_date": "2024-01-01T00:00:00+00:00",
            "department": "Test",
            "purpose": "Test",
            "release_id": "id_2024",
        },
    )
    assert response.status_code == 422


def test_upsert_record_201_new_nca_after_previous_upsert(client):
    response1 = client.post(
        "/pipeline/records",
        json={
            "nca_number": "NCA-SEQ-99-0000999",
            "nca_type": "REG",
            "released_date": "2024-01-01T00:00:00+00:00",
            "department": "First",
            "purpose": "First",
            "release_id": "id_2024",
        },
    )
    assert response1.status_code == 201

    response2 = client.post(
        "/pipeline/records",
        json={
            "nca_number": "NCA-SEQ-99-0000999",
            "nca_type": "REG",
            "released_date": "2025-01-01T00:00:00+00:00",
            "department": "Second",
            "purpose": "Second",
            "release_id": "id_2025",
        },
    )
    assert response2.status_code == 200
    assert response2.json()["department"] == "Second"
