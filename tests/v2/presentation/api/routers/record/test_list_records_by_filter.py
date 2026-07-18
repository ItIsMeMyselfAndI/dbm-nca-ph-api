from src.core.entities.record_filter import RecordFilter

FILTER_KEY = RecordFilter.DEPARTMENT
FILTER_VALUE = "Department of Education (DepEd)"
TOTAL_MATCHING = 398

FIRST_MATCH_ID = "7036805d-779d-41b7-94ed-0156779a1ed5"


def test_list_records_by_filter(client):
    response = client.get(f"/records/{FILTER_KEY.value}/{FILTER_VALUE}?limit=10")
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert data["count"] == 10
    assert data["cursor"] is None
    assert data["next_cursor"] is not None


def test_list_records_by_filter_by_nca_type(client):
    response = client.get("/records/nca_type/TLRG?limit=20")
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert data["count"] == 13
    for item in data["items"]:
        assert item["nca_type"] == "TLRG"


def test_list_records_by_filter_with_default_limit(client):
    response = client.get(f"/records/{FILTER_KEY.value}/{FILTER_VALUE}")
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert data["count"] == 20


def test_list_records_by_filter_with_cursor(client):
    response = client.get(f"/records/{FILTER_KEY.value}/{FILTER_VALUE}?limit=5")
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert data["count"] == 5
    assert data["cursor"] is None
    assert data["next_cursor"] is not None

    response_next = client.get(
        f"/records/{FILTER_KEY.value}/{FILTER_VALUE}?limit=5&cursor={data['next_cursor']}"
    )
    assert response_next.status_code == 200
    data_next = response_next.json()
    assert "items" in data_next
    assert data_next["count"] == 5
    assert data_next["cursor"] == data["next_cursor"]
    assert data_next["next_cursor"] is not None


def test_list_records_by_filter_with_invalid_cursor(client):
    response = client.get(
        f"/records/{FILTER_KEY.value}/{FILTER_VALUE}?limit=5&cursor=nonexistent-id"
    )
    assert response.status_code == 200
    data = response.json()
    assert data["count"] == 0


def test_list_records_by_filter_with_empty_cursor(client):
    response = client.get(f"/records/{FILTER_KEY.value}/{FILTER_VALUE}?limit=5&cursor=")
    assert response.status_code == 400


def test_list_records_by_filter_with_leading_trailing_spaces_cursor(client):
    cursor = f" {FIRST_MATCH_ID} "
    response = client.get(
        f"/records/{FILTER_KEY.value}/{FILTER_VALUE}?limit=5&cursor={cursor}"
    )
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert data["count"] == 5
    assert data["cursor"] == cursor
    assert data["next_cursor"] is not None


def test_list_records_by_filter_with_upper_case_cursor(client):
    cursor = FIRST_MATCH_ID.upper()
    response = client.get(
        f"/records/{FILTER_KEY.value}/{FILTER_VALUE}?limit=5&cursor={cursor}"
    )
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert data["count"] == 5
    assert data["cursor"] == cursor
    assert data["next_cursor"] is not None


def test_list_records_by_filter_with_limit_zero(client):
    response = client.get(f"/records/{FILTER_KEY.value}/{FILTER_VALUE}?limit=0")
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert data["count"] == 0
    assert data["cursor"] is None
    assert data["next_cursor"] is None


def test_list_records_by_filter_with_limit_exceeding_total(client):
    response = client.get(f"/records/{FILTER_KEY.value}/{FILTER_VALUE}?limit=2000")
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert data["count"] == TOTAL_MATCHING
    assert data["cursor"] is None
    assert data["next_cursor"] is not None


def test_list_records_by_filter_with_negative_limit(client):
    response = client.get(f"/records/{FILTER_KEY.value}/{FILTER_VALUE}?limit=-5")
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert data["count"] == 0
    assert data["cursor"] is None
    assert data["next_cursor"] is None


def test_list_records_by_filter_with_no_matching_records(client):
    response = client.get(
        f"/records/{FILTER_KEY.value}/Nonexistent+Department?limit=10"
    )
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert data["count"] == 0
    assert data["cursor"] is None
    assert data["next_cursor"] is None
