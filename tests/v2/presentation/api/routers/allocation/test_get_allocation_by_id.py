def test_get_allocation_by_id(client):
    response = client.get("/allocations/0000a66b-0265-4b42-adfe-559f98646c91")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == "0000a66b-0265-4b42-adfe-559f98646c91"


def test_get_allocation_by_id_not_found(client):
    response = client.get("/allocations/nonexistent-id")
    assert response.status_code == 404


def test_get_allocation_by_id_in_upper_case(client):
    response = client.get("/allocations/0000A66B-0265-4B42-ADFE-559F98646C91")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == "0000a66b-0265-4b42-adfe-559f98646c91"


def test_get_allocation_by_id_leading_trailing_spaces(client):
    response = client.get("/allocations/ 0000a66b-0265-4b42-adfe-559f98646c91 ")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == "0000a66b-0265-4b42-adfe-559f98646c91"


def test_get_allocation_by_id_empty_string(client):
    response = client.get("/allocations/")
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert data["cursor"] is None
    assert data["next_cursor"] is not None
