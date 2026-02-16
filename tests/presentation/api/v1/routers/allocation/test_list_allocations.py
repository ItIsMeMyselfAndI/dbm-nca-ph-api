def test_list_allocations(client):
    reponse = client.get("/allocations?limit=10")
    assert reponse.status_code == 200
    data = reponse.json()
    assert "items" in data
    assert data["count"] == 10
    assert data["cursor"] is None
    assert data["next_cursor"] is not None


def test_list_allocations_with_cursor(client):
    response = client.get("/allocations?limit=5")
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert data["count"] == 5
    assert data["cursor"] is None
    assert data["next_cursor"] is not None

    response_next = client.get(f"/allocations?limit=5&cursor={data['next_cursor']}")
    assert response_next.status_code == 200
    data_next = response_next.json()
    assert "items" in data_next
    assert data_next["count"] == 5
    assert data_next["cursor"] == data["next_cursor"]
    assert data_next["next_cursor"] is not None


def test_list_allocations_with_invalid_cursor(client):
    response = client.get("/allocations?cursor=nonexistent-id")
    assert response.status_code == 404


def test_list_allocations_with_empty_cursor(client):
    response = client.get("/allocations?cursor=")
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert data["count"] == 20
    assert data["cursor"] == ""
    assert data["next_cursor"] is not None


def test_list_allocations_with_leading_trailing_spaces_cursor(client):
    response = client.get(
        "/allocations?limit=5&cursor= 00002e59-c77c-46b3-8068-f49e33f3674c "
    )
    assert response.status_code == 404


def test_list_allocations_with_case_sensitivity_cursor(client):
    response = client.get(
        "/allocations?limit=5&cursor=00002E59-C77C-46B3-8068-F49E33F3674C"
    )
    assert response.status_code == 404


def test_list_allocations_with_limit_zero(client):
    response = client.get("/allocations?limit=0")
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert len(data["items"]) == 0
    assert data["count"] == 0
    assert data["cursor"] is None
    assert data["next_cursor"] is None


def test_list_allocations_with_limit_exceeding_total(client):
    response = client.get("/allocations?limit=100")
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert len(data["items"]) == 40
    assert data["count"] == 40
    assert data["cursor"] is None
    assert data["next_cursor"] is None


def test_list_allocations_with_negative_limit(client):
    response = client.get("/allocations?limit=-5")
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert len(data["items"]) == 0
    assert data["count"] == 0
    assert data["cursor"] is None
    assert data["next_cursor"] is None
