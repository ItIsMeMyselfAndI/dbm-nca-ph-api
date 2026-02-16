def test_list_allocations_by_filter(client):
    response = client.get(
        "/allocations/operating_unit/Coron School of Fisheries?limit=10"
    )
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert data["count"] == 1
    assert data["cursor"] is None
    assert data["next_cursor"] is None
    assert len(data["items"]) == 1
    for allocation in data["items"]:
        assert allocation["operating_unit"] == "Coron School of Fisheries"


def test_list_allocations_by_filter_with_cursor(client):
    response = client.get(
        "/allocations/operating_unit/Coron School of Fisheries?limit=5"
    )
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert data["count"] == 1
    assert data["cursor"] is None
    assert data["next_cursor"] is None
    assert len(data["items"]) == 1
    for allocation in data["items"]:
        assert allocation["operating_unit"] == "Coron School of Fisheries"
    # assert second_page[0].operating_unit == "Coron School of Fisheries"


def test_list_allocations_by_filter_with_invalid_cursor(client):
    response = client.get(
        "/allocations/operating_unit/Coron School of Fisheries?limit=5&cursor=nonexistent-id"
    )
    assert response.status_code == 404


def test_list_allocations_by_filter_with_empty_cursor(client):
    response = client.get(
        "/allocations/operating_unit/Coron School of Fisheries?limit=5&cursor="
    )
    assert response.status_code == 404


def test_list_allocations_by_filter_with_leading_trailing_spaces_cursor(client):
    response = client.get(
        "/allocations/operating_unit/Coron School of Fisheries?limit=5&cursor= 00002e59-c77c-46b3-8068-f49e33f3674c "
    )
    assert response.status_code == 404


def test_list_allocations_by_filter_with_case_sensitivity_cursor(client):
    response = client.get(
        "/allocations/operating_unit/Coron School of Fisheries?limit=5&cursor=00002E59-C77C-46B3-8068-F49E33F3674C"
    )
    assert response.status_code == 404


def test_list_allocations_by_filter_with_limit_zero(client):
    response = client.get(
        "/allocations/operating_unit/Coron School of Fisheries?limit=0"
    )
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert len(data["items"]) == 0
    assert data["count"] == 0
    assert data["cursor"] is None
    assert data["next_cursor"] is None


def test_list_allocations_by_filter_with_limit_exceeding_total(client):
    response = client.get(
        "/allocations/operating_unit/Coron School of Fisheries?limit=100"
    )
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert len(data["items"]) == 1
    assert data["count"] == 1
    assert data["cursor"] is None
    assert data["next_cursor"] is None


def test_list_allocations_by_filter_with_negative_limit(client):
    response = client.get(
        "/allocations/operating_unit/Coron School of Fisheries?limit=-5"
    )
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert len(data["items"]) == 0
    assert data["count"] == 0
    assert data["cursor"] is None
    assert data["next_cursor"] is None


def test_list_allocations_by_filter_with_no_matching_records(client):
    response = client.get(
        "/allocations/operating_unit/Nonexistent Operating Unit?limit=10"
    )
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert len(data["items"]) == 0
    assert data["count"] == 0
    assert data["cursor"] is None
    assert data["next_cursor"] is None
