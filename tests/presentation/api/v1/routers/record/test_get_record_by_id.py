def test_get_record_by_id(client):
    response = client.get("/records/91e80926-ea6a-48d1-bb63-875b4924ecec")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == "91e80926-ea6a-48d1-bb63-875b4924ecec"
    assert data["nca_number"] == "NCA-ROIX-24-0000001"
    assert data["nca_type"] == "REG"
    assert data["released_date"] == "2024-01-02T07:10:16+00:00"
    assert data["department"] == "Department of Health (DOH)"
    assert (
        data["purpose"]
        == "To cover the regular operating and RLIP requirements for the first quarter (January to March 2024)"
    )
    assert data["release_id"] == "id_2024"


def test_get_record_by_id_not_found(client):
    response = client.get("/records/nonexistent-id")
    assert response.status_code == 404


def test_get_record_by_id_empty_string(client):
    response = client.get("/records/")  # hits the list_records endpoint instead
    assert response.status_code == 200
    data = response.json()
    assert "items" in data


def test_get_record_by_id_case_sensitivity(client):
    response = client.get("/records/91E80926-EA6A-48D1-BB63-875B4924ECEC")
    assert response.status_code == 404


def test_get_record_by_id_leading_trailing_spaces(client):
    response = client.get("/records/ 91e80926-ea6a-48d1-bb63-875b4924ecec ")
    assert response.status_code == 404
