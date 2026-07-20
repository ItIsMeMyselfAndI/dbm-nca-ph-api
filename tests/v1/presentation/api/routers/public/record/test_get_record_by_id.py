def test_get_record_by_id(client):
    response = client.get("/records/91e80926-ea6a-48d1-bb63-875b4924ecec")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == "91e80926-ea6a-48d1-bb63-875b4924ecec"


def test_get_record_by_id_not_found(client):
    response = client.get("/records/nonexistent-id")
    assert response.status_code == 404


def test_get_record_by_id_empty_string(client):
    response = client.get("/records/")  # hits the list_records endpoint instead
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert data["count"] == 20
    assert data["cursor"] is None
    assert data["next_cursor"] is not None


def test_get_record_by_id_in_upper_case(client):
    response = client.get("/records/91E80926-EA6A-48D1-BB63-875B4924ECEC")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == "91e80926-ea6a-48d1-bb63-875b4924ecec"


def test_get_record_by_id_leading_trailing_spaces(client):
    response = client.get("/records/ 91e80926-ea6a-48d1-bb63-875b4924ecec ")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == "91e80926-ea6a-48d1-bb63-875b4924ecec"
