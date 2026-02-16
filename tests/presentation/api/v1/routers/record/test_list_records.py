def test_list_records(client):
    response = client.get("/records?limit=10")
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert data["count"] == 10
    assert data["cursor"] is None
    assert data["next_cursor"] is not None


def test_list_records_with_cursor(client):
    response = client.get("/records?limit=5")
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert data["count"] == 5
    assert data["cursor"] is None
    assert data["next_cursor"] is not None

    response_next = client.get(f"/records?limit=5&cursor={data['next_cursor']}")
    assert response_next.status_code == 200
    data_next = response_next.json()
    assert "items" in data_next
    assert data_next["count"] == 5
    assert data_next["cursor"] == data["next_cursor"]
    assert data_next["next_cursor"] is not None


def test_list_records_with_invalid_cursor(client):
    response = client.get("/records?cursor=nonexistent-id")
    assert response.status_code == 404


def test_list_records_with_empty_cursor(client):
    response = client.get("/records?cursor=")
    assert response.status_code == 404


def test_list_records_with_leading_trailing_spaces_cursor(client):
    response = client.get(
        "/records?limit=5&cursor= 91e80926-ea6a-48d1-bb63-875b4924ecec "
    )
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert data["count"] == 5
    assert data["cursor"] is not None
    assert data["next_cursor"] is not None


def test_list_records_with_upper_case_cursor(client):
    response = client.get(
        "/records?limit=5&cursor=91E80926-EA6A-48D1-BB63-875B4924ECEC"
    )
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert data["count"] == 5
    assert data["cursor"] is not None
    assert data["next_cursor"] is not None


def test_list_records_with_limit_zero(client):
    response = client.get("/records?limit=0")
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert data["count"] == 0
    assert data["cursor"] is None
    assert data["next_cursor"] is None


def test_list_records_with_limit_exceeding_total(client):
    response = client.get("/records?limit=100")
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert data["count"] == 40
    assert data["cursor"] is None
    assert data["next_cursor"] is None


def test_list_records_with_negative_limit(client):
    response = client.get("/records?limit=-5")
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert data["count"] == 0
    assert data["cursor"] is None
    assert data["next_cursor"] is None
