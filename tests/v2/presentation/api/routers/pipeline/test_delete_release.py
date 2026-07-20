def test_delete_release_204(client):
    response = client.delete("/pipeline/releases/id_2024")
    assert response.status_code == 204
    assert response.text == ""


def test_delete_release_404(client):
    response = client.delete("/pipeline/releases/nonexistent-id")
    assert response.status_code == 404


def test_delete_release_then_get_returns_404(client):
    response = client.delete("/pipeline/releases/id_2025")
    assert response.status_code == 204

    get_response = client.get("/releases/id_2025")
    assert get_response.status_code == 404


def test_delete_release_id_with_special_chars(client):
    response = client.delete("/pipeline/releases/id_2026")
    assert response.status_code == 204
