def test_get_allocation_by_id(client):
    response = client.get("/allocations/00002e59-c77c-46b3-8068-f49e33f3674c")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == "00002e59-c77c-46b3-8068-f49e33f3674c"


def test_get_allocation_by_id_not_found(client):
    response = client.get("/allocations/nonexistent-id")
    assert response.status_code == 404


def test_get_allocation_by_id_empty_string(client):
    response = client.get("/allocations/")  # hit the list endpoint instead
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert data["cursor"] is None
    assert data["next_cursor"] is not None


def test_get_allocation_by_id_in_upper_case(client):
    reponse = client.get("/allocations/00002E59-C77C-46B3-8068-F49E33F3674C")
    assert reponse.status_code == 200
    data = reponse.json()
    assert data["id"] == "00002e59-c77c-46b3-8068-f49e33f3674c"


def test_get_allocation_by_id_leading_trailing_spaces(client):
    response = client.get("/allocations/ 00002e59-c77c-46b3-8068-f49e33f3674c ")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == "00002e59-c77c-46b3-8068-f49e33f3674c"
