def test_upsert_release_201(client):
    response = client.post(
        "/pipeline/releases",
        json={
            "id": "new-release-test",
            "title": "Test Release",
            "url": "https://example.com/test.pdf",
            "filename": "test.pdf",
            "year": 2026,
            "page_count": 10,
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["id"] == "new-release-test"
    assert data["title"] == "Test Release"
    assert data["year"] == 2026
    assert data["page_count"] == 10


def test_upsert_release_200(client):
    response = client.post(
        "/pipeline/releases",
        json={
            "id": "id_2024",
            "title": "Updated Release",
            "url": "https://example.com/updated.pdf",
            "filename": "updated.pdf",
            "year": 2024,
            "page_count": 99,
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == "id_2024"
    assert data["title"] == "Updated Release"
    assert data["page_count"] == 99


def test_upsert_release_422_empty_body(client):
    response = client.post("/pipeline/releases", json={})
    assert response.status_code == 422


def test_upsert_release_422_missing_required_fields(client):
    response = client.post(
        "/pipeline/releases",
        json={"id": "partial"},
    )
    assert response.status_code == 422


def test_upsert_release_default_page_count(client):
    response = client.post(
        "/pipeline/releases",
        json={
            "id": "release-no-page-count",
            "title": "No Page Count",
            "url": "https://example.com/nopc.pdf",
            "filename": "nopc.pdf",
            "year": 2026,
        },
    )
    assert response.status_code == 201
    assert response.json()["page_count"] == 0
