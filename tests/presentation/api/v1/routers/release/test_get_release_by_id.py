def test_get_release_by_id(client):
    response = client.get("/releases/id_2024")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == "id_2024"
    assert data["year"] == 2024
    assert (
        data["url"] == "https://www.dbm.gov.ph/wp-content/uploads/NCA/2024/NCA_2024.pdf"
    )
    assert data["filename"] == "NCA_2024.pdf"


def test_get_release_by_id_not_found(client):
    response = client.get("/releases/nonexistent-id")
    assert response.status_code == 404


def test_get_release_by_id_empty_string(client):
    response = client.get("/releases/")  # hits the list_releases endpoint instead
    assert response.status_code == 200
    data = response.json()
    assert "items" in data


def test_get_release_by_id_case_sensitivity(client):
    response = client.get("/releases/ID_2024")
    assert response.status_code == 404


def test_get_release_by_id_leading_trailing_spaces(client):
    response = client.get("/releases/ id_2024 ")
    assert response.status_code == 404
