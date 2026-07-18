from src.core.entities.allocation_filter import AllocationFilter

FILTER_KEY = AllocationFilter.OPERATING_UNIT
FILTER_VALUE = "Engr. Virgilio V. Dionisio Memorial School"


MATCHING_ALLOCATION_ID = "0318b06b-d007-4f40-a257-ae98a9036609"


def test_list_allocations_by_filter(client):
    response = client.get(f"/allocations/{FILTER_KEY.value}/{FILTER_VALUE}?limit=10")
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert data["count"] == 1
    assert data["cursor"] is None
    assert data["next_cursor"] == MATCHING_ALLOCATION_ID


def test_list_allocations_by_filter_by_agency(client):
    response = client.get(
        "/allocations/agency/Foreign Service Institute?limit=10"
    )
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert data["count"] == 1
    assert data["items"][0]["agency"] == "Foreign Service Institute"
    assert data["cursor"] is None
    assert data["next_cursor"] == "000f2814-0615-4cdc-a733-285e55f728ef"


def test_list_allocations_by_filter_with_default_limit(client):
    response = client.get(
        f"/allocations/{FILTER_KEY.value}/{FILTER_VALUE}"
    )
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert data["count"] == 1


def test_list_allocations_by_filter_with_cursor(client):
    response = client.get(
        (
            f"/allocations/{FILTER_KEY.value}/{FILTER_VALUE}?limit=5&"
            f"cursor={MATCHING_ALLOCATION_ID}"
        )
    )
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert data["count"] == 0
    assert data["cursor"] == MATCHING_ALLOCATION_ID
    assert data["next_cursor"] is None


def test_list_allocations_by_filter_with_invalid_cursor(client):
    response = client.get(
        f"/allocations/{FILTER_KEY.value}/{FILTER_VALUE}?limit=5&cursor=nonexistent-id"
    )
    assert response.status_code == 404


def test_list_allocations_by_filter_with_empty_cursor(client):
    response = client.get(
        f"/allocations/{FILTER_KEY.value}/{FILTER_VALUE}?limit=5&cursor="
    )
    assert response.status_code == 404


def test_list_allocations_by_filter_with_leading_trailing_spaces_cursor(client):
    cursor = f" {MATCHING_ALLOCATION_ID} "
    response = client.get(
        f"/allocations/{FILTER_KEY.value}/{FILTER_VALUE}?limit=5&cursor={cursor}"
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
        f"/allocations/{FILTER_KEY.value}/{FILTER_VALUE}?limit=5&cursor={cursor}"
    )
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert data["count"] == 0
    assert data["cursor"] == cursor
    assert data["next_cursor"] is None


def test_list_allocations_by_filter_with_limit_zero(client):
    response = client.get(f"/allocations/{FILTER_KEY.value}/{FILTER_VALUE}?limit=0")
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert len(data["items"]) == 0
    assert data["count"] == 0
    assert data["cursor"] is None
    assert data["next_cursor"] is None


def test_list_allocations_by_filter_with_limit_exceeding_total(client):
    response = client.get(f"/allocations/{FILTER_KEY.value}/{FILTER_VALUE}?limit=100")
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert data["count"] == 1
    assert data["cursor"] is None
    assert data["next_cursor"] == MATCHING_ALLOCATION_ID


def test_list_allocations_by_filter_with_negative_limit(client):
    response = client.get(f"/allocations/{FILTER_KEY.value}/{FILTER_VALUE}?limit=-5")
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert data["count"] == 0
    assert data["cursor"] is None
    assert data["next_cursor"] is None


def test_list_allocations_by_filter_with_no_matching_records(client):
    response = client.get(
        f"/allocations/{FILTER_KEY.value}/Nonexistent Operating Unit?limit=10"
    )
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert data["count"] == 0
    assert data["cursor"] is None
    assert data["next_cursor"] is None
