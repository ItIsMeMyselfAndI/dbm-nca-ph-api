def test_delete_allocation_204(client):
    existing = client.get("/allocations?limit=1").json()["items"][0]

    response = client.delete(f"/pipeline/allocations/{existing['id']}")
    assert response.status_code == 204
    assert response.text == ""


def test_delete_allocation_404(client):
    response = client.delete("/pipeline/allocations/nonexistent-id")
    assert response.status_code == 404


def test_delete_allocation_then_get_returns_404(client):
    existing = client.get("/allocations?limit=1").json()["items"][0]
    alloc_id = existing["id"]

    delete_resp = client.delete(f"/pipeline/allocations/{alloc_id}")
    assert delete_resp.status_code == 204

    get_resp = client.get(f"/allocations/{alloc_id}")
    assert get_resp.status_code == 404


def test_delete_allocation_with_uuid_id(client):
    existing = client.get("/allocations?limit=1").json()["items"][0]

    response = client.delete(f"/pipeline/allocations/{existing['id']}")
    assert response.status_code == 204
