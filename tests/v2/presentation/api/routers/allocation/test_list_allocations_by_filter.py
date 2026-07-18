def test_list_allocations_by_filter(client):
    response = client.get("/allocations/nca_number/NCA-NCR-25-0001001?limit=10")
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert data["count"] <= 10


def test_list_allocations_by_filter_with_empty_cursor(client):
    response = client.get("/allocations/nca_number/NCA-NCR-25-0001001?cursor=")
    assert response.status_code == 400
