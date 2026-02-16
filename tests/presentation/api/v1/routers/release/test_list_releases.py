def test_list_releases(client):
    response = client.get("/releases?limit=10")
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert data["count"] == 3
    assert data["cursor"] is None
    assert data["next_cursor"] is None


def test_list_releases_with_cursor(client):
    response = client.get("/releases?limit=2")
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert data["count"] == 2
    assert data["cursor"] is None
    assert data["next_cursor"] is not None

    response_next = client.get(f"/releases?limit=2&cursor={data['next_cursor']}")
    assert response_next.status_code == 200
    data_next = response_next.json()
    assert "items" in data_next
    assert data_next["count"] == 1
    assert data_next["cursor"] == data["next_cursor"]
    assert data_next["next_cursor"] is None


def test_list_releases_with_invalid_cursor(client):
    response = client.get("/releases?limit=2&cursor=nonexistent-id")
    assert response.status_code == 404


def test_list_releases_with_empty_cursor(client):
    response = client.get("/releases?limit=2&cursor=")
    assert response.status_code == 404


def test_list_releases_with_leading_trailing_spaces_cursor(client):
    response = client.get("/releases?limit=2&cursor= id_2024 ")
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert data["count"] == 2
    assert data["cursor"] is not None
    assert data["next_cursor"] is not None


def test_list_releases_with_upper_case_cursor(client):
    response = client.get("/releases?limit=2&cursor=ID_2024")
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert data["count"] == 2
    assert data["cursor"] is not None
    assert data["next_cursor"] is not None


def test_list_releases_with_limit_zero(client):
    response = client.get("/releases?limit=0")
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert data["count"] == 0
    assert data["cursor"] is None
    assert data["next_cursor"] is None


def test_list_releases_with_limit_exceeding_total(client):
    response = client.get("/releases?limit=10")
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert data["count"] == 3
    assert data["cursor"] is None
    assert data["next_cursor"] is None


def test_list_releases_with_negative_limit(client):
    response = client.get("/releases?limit=-5")
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert data["count"] == 0
    assert data["cursor"] is None
    assert data["next_cursor"] is None
