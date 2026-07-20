def test_delete_record_204(client):
    existing_nca = client.get("/records?limit=1").json()["items"][0]["nca_number"]

    response = client.delete(f"/pipeline/records/{existing_nca}")
    assert response.status_code == 204
    assert response.text == ""


def test_delete_record_404(client):
    response = client.delete("/pipeline/records/NCA-NONEXISTENT-99-9999999")
    assert response.status_code == 404


def test_delete_record_then_get_returns_404(client):
    existing = client.get("/records?limit=1").json()["items"][0]
    nca = existing["nca_number"]
    record_id = existing["id"]

    delete_resp = client.delete(f"/pipeline/records/{nca}")
    assert delete_resp.status_code == 204

    get_resp = client.get(f"/records/{record_id}")
    assert get_resp.status_code == 404


def test_delete_record_with_nca_number_containing_slashes(client):
    response = client.delete("/pipeline/records/NCA-ROIX-24-0000002")
    assert response.status_code == 204
