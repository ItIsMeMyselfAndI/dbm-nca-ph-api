def test_get_release_by_id(client):
    response = client.get("/releases/id_2024")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == "id_2024"


def test_get_release_by_id_not_found(client):
    response = client.get("/releases/nonexistent-id")
    assert response.status_code == 404


def test_get_release_by_id_in_upper_case(client):
    response = client.get("/releases/ID_2024")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == "id_2024"


def test_get_release_by_id_leading_trailing_spaces(client):
    response = client.get("/releases/ id_2024 ")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == "id_2024"
