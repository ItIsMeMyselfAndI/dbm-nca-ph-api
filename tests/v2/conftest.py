import pytest
from fastapi.testclient import TestClient

from main import app
from src.presentation.api.auth import require_pipeline_key
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


def _bypass_pipeline_key() -> None:
    return None


@pytest.fixture
def mock_release_repository():
    return MockAsyncReleaseRepository()


@pytest.fixture
def mock_record_repository():
    return MockAsyncRecordRepository()


@pytest.fixture
def mock_allocation_repository():
    return MockAsyncAllocationRepository()


@pytest.fixture
def client(mock_allocation_repository, mock_record_repository, mock_release_repository):
    app.dependency_overrides[get_allocation_repository] = (
        lambda: mock_allocation_repository
    )
    app.dependency_overrides[get_record_repository] = lambda: mock_record_repository
    app.dependency_overrides[get_release_repository] = lambda: mock_release_repository
    app.dependency_overrides[require_pipeline_key] = lambda: _bypass_pipeline_key()

    with TestClient(app, base_url="http://testserver/api/v2") as c:
        yield c

    app.dependency_overrides = {}
