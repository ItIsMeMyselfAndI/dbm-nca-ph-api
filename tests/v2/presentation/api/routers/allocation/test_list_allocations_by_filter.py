FILTER_KEY = "operating_unit"
FILTER_VALUE = "Tigwi National High School"

MATCHING_ALLOCATION_ID = "0000a66b-0265-4b42-adfe-559f98646c91"


def test_list_allocations_by_filter(client):
    response = client.get(f"/allocations/{FILTER_KEY}/{FILTER_VALUE}?limit=10")
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert data["count"] == 1
    assert data["cursor"] is None
    assert data["next_cursor"] == MATCHING_ALLOCATION_ID


def test_list_allocations_by_filter_by_agency(client):
    response = client.get("/allocations/agency/Bureau%20of%20the%20Treasury?limit=10")
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert data["count"] == 7
    for item in data["items"]:
        assert item["agency"] == "Bureau of the Treasury"
    assert data["cursor"] is None


def test_list_allocations_by_filter_with_default_limit(client):
    response = client.get(f"/allocations/{FILTER_KEY}/{FILTER_VALUE}")
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert data["count"] == 1


def test_list_allocations_by_filter_with_cursor(client):
    response = client.get(
        f"/allocations/{FILTER_KEY}/{FILTER_VALUE}?limit=5&cursor={MATCHING_ALLOCATION_ID}"
    )
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert data["count"] == 0
    assert data["cursor"] == MATCHING_ALLOCATION_ID
    assert data["next_cursor"] is None


def test_list_allocations_by_filter_with_invalid_cursor(client):
    response = client.get(
        f"/allocations/{FILTER_KEY}/{FILTER_VALUE}?limit=5&cursor=nonexistent-id"
    )
    assert response.status_code == 200
    data = response.json()
    assert data["count"] == 0


def test_list_allocations_by_filter_with_empty_cursor(client):
    response = client.get(f"/allocations/{FILTER_KEY}/{FILTER_VALUE}?limit=5&cursor=")
    assert response.status_code == 400


def test_list_allocations_by_filter_with_leading_trailing_spaces_cursor(client):
    cursor = f" {MATCHING_ALLOCATION_ID} "
    response = client.get(
        f"/allocations/{FILTER_KEY}/{FILTER_VALUE}?limit=5&cursor={cursor}"
    )
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert data["count"] == 0
    assert data["cursor"] == cursor
    assert data["next_cursor"] is None


def test_list_allocations_by_filter_with_upper_case_cursor(client):
    cursor = MATCHING_ALLOCATION_ID.upper()
    response = client.get(
        f"/allocations/{FILTER_KEY}/{FILTER_VALUE}?limit=5&cursor={cursor}"
    )
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert data["count"] == 0
    assert data["cursor"] == cursor
    assert data["next_cursor"] is None


def test_list_allocations_by_filter_with_limit_zero(client):
    response = client.get(f"/allocations/{FILTER_KEY}/{FILTER_VALUE}?limit=0")
    assert response.status_code == 200
    data = response.json()
    assert len(data["items"]) == 0
    assert data["count"] == 0
    assert data["cursor"] is None
    assert data["next_cursor"] is None


def test_list_allocations_by_filter_with_limit_exceeding_total(client):
    response = client.get(f"/allocations/{FILTER_KEY}/{FILTER_VALUE}?limit=100")
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert data["count"] == 1
    assert data["cursor"] is None
    assert data["next_cursor"] == MATCHING_ALLOCATION_ID


def test_list_allocations_by_filter_with_negative_limit(client):
    response = client.get(f"/allocations/{FILTER_KEY}/{FILTER_VALUE}?limit=-5")
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert data["count"] == 0
    assert data["cursor"] is None
    assert data["next_cursor"] is None


def test_list_allocations_by_filter_with_no_matching_records(client):
    response = client.get(
        f"/allocations/{FILTER_KEY}/Nonexistent+Operating+Unit?limit=10"
    )
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert data["count"] == 0
    assert data["cursor"] is None
    assert data["next_cursor"] is None
