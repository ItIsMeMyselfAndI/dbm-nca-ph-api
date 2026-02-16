def test_list_records_by_filter(client):
    reponse = client.get("/records/department/Department of Health (DOH)?limit=10")
    assert reponse.status_code == 200
    data = reponse.json()
    assert "items" in data
    assert data["count"] == 6
    assert data["cursor"] is None
    assert data["next_cursor"] is None


def test_list_records_by_filter_with_cursor(client):
    response = client.get("/records/department/Department of Health (DOH)?limit=5")
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert data["count"] == 5
    assert data["cursor"] is None
    assert data["next_cursor"] is not None

    response_next = client.get(
        f"/records/department/Department of Health (DOH)?limit=5&cursor={data['next_cursor']}"
    )
    assert response_next.status_code == 200
    data_next = response_next.json()
    assert "items" in data_next
    assert data_next["count"] == 1
    assert data_next["cursor"] == data["next_cursor"]
    assert data_next["next_cursor"] is None


def test_list_records_by_filter_with_invalid_cursor(client):
    response = client.get(
        "/records/department/Department of Health (DOH)?limit=5&cursor=nonexistent-id"
    )
    assert response.status_code == 404


def test_list_records_by_filter_with_empty_cursor(client):
    response = client.get(
        "/records/department/Department of Health (DOH)?limit=5&cursor="
    )
    assert response.status_code == 404


def test_list_records_by_filter_with_leading_trailing_spaces_cursor(client):
    response = client.get(
        "/records/department/Department of Health (DOH)?limit=5&cursor= 91e80926-ea6a-48d1-bb63-875b4924ecec "
    )
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert data["count"] == 5
    assert data["cursor"] is not None
    assert data["next_cursor"] is not None


def test_list_records_by_filter_with_upper_case_cursor(client):
    response = client.get(
        "/records/department/Department of Health (DOH)?limit=5&cursor=91E80926-EA6A-48D1-BB63-875B4924ECEC"
    )
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert data["count"] == 5
    assert data["cursor"] is not None
    assert data["next_cursor"] is not None


def test_list_records_by_filter_with_limit_zero(client):
    response = client.get("/records/department/Department of Health (DOH)?limit=0")
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert data["count"] == 0
    assert data["cursor"] is None
    assert data["next_cursor"] is None


def test_list_records_by_filter_with_limit_exceeding_total(client):
    response = client.get("/records/department/Department of Health (DOH)?limit=100")
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert data["count"] == 6
    assert data["cursor"] is None
    assert data["next_cursor"] is None


def test_list_records_by_filter_with_negative_limit(client):
    response = client.get("/records/department/Department of Health (DOH)?limit=-5")
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert data["count"] == 0
    assert data["cursor"] is None
    assert data["next_cursor"] is None


def test_list_records_by_filter_with_no_matching_records(client):
    response = client.get("/records/department/Nonexistent Department?limit=10")
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert data["count"] == 0
    assert data["cursor"] is None
    assert data["next_cursor"] is None
