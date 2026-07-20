import pytest
from fastapi.testclient import TestClient

from main import app
from src.infrastructure.config import settings
from src.presentation.api.dependencies_v2 import (
    get_allocation_repository,
    get_record_repository,
    get_release_repository,
)
from tests.mock.repositories_async.mock_async_allocation_repository import (
    MockAsyncAllocationRepository,
)
from tests.mock.repositories_async.mock_async_record_repository import (
    MockAsyncRecordRepository,
)
from tests.mock.repositories_async.mock_async_release_repository import (
    MockAsyncReleaseRepository,
)


@pytest.fixture
def client():
    app.dependency_overrides[get_allocation_repository] = lambda: MockAsyncAllocationRepository()
    app.dependency_overrides[get_record_repository] = lambda: MockAsyncRecordRepository()
    app.dependency_overrides[get_release_repository] = lambda: MockAsyncReleaseRepository()
    with TestClient(app, base_url="http://testserver/api/v2") as c:
        yield c
    app.dependency_overrides = {}


def test_pipeline_missing_api_key(client):
    response = client.post("/pipeline/releases", json={})
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid API key"


def test_pipeline_invalid_api_key(client):
    response = client.post(
        "/pipeline/releases",
        json={},
        headers={"X-API-Key": "wrong-key"},
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid API key"


def test_pipeline_empty_api_key(client):
    response = client.post(
        "/pipeline/releases",
        json={},
        headers={"X-API-Key": ""},
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid API key"


def test_pipeline_valid_api_key(client):
    response = client.post(
        "/pipeline/releases",
        json={"id": "test-auth", "title": "t", "url": "u", "filename": "f", "year": 2026},
        headers={"X-API-Key": settings.PIPELINE_API_KEY},
    )
    assert response.status_code == 201


def test_pipeline_delete_with_valid_key(client):
    response = client.delete(
        "/pipeline/releases/id_2024",
        headers={"X-API-Key": settings.PIPELINE_API_KEY},
    )
    assert response.status_code == 204


def test_pipeline_delete_without_key(client):
    response = client.delete("/pipeline/releases/id_2024")
    assert response.status_code == 401


def test_pipeline_post_records_without_key(client):
    response = client.post("/pipeline/records", json={})
    assert response.status_code == 401


def test_pipeline_post_allocations_without_key(client):
    response = client.post("/pipeline/allocations", json={})
    assert response.status_code == 401


def test_pipeline_all_methods_required_key(client):
    endpoints = [
        ("POST", "/pipeline/releases"),
        ("DELETE", "/pipeline/releases/id_2024"),
        ("POST", "/pipeline/records"),
        ("DELETE", "/pipeline/records/NCA-TEST"),
        ("POST", "/pipeline/allocations"),
        ("DELETE", "/pipeline/allocations/some-id"),
    ]
    for method, path in endpoints:
        response = client.request(method, path)
        assert response.status_code == 401, f"{method} {path} should return 401"
