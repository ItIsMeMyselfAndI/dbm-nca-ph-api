def test_list_records_by_filter(client):
    response = client.get("/records/nca_type/REG?limit=10")
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert data["count"] <= 10


def test_list_records_by_filter_with_empty_cursor(client):
    response = client.get("/records/nca_type/REG?cursor=")
    assert response.status_code == 400
