import pytest
from fastapi.testclient import TestClient

from src.main import app
from src.presentation.api.dependencies import (
    get_allocation_repository,
    get_record_repository,
    get_release_repository,
)
from tests.infrastructure.db.allocation.mock_allocation_repository import (
    MockAllocationRepository,
)
from tests.infrastructure.db.record.mock_record_repository import MockRecordRepository
from tests.infrastructure.db.release.mock_release_repository import (
    MockReleaseRepository,
)


@pytest.fixture
def mock_release_repository():
    return MockReleaseRepository()


@pytest.fixture
def mock_record_repository():
    return MockRecordRepository()


@pytest.fixture
def mock_allocation_repository():
    return MockAllocationRepository()


@pytest.fixture
def client(mock_allocation_repository, mock_record_repository, mock_release_repository):
    app.dependency_overrides[get_allocation_repository] = (
        lambda: mock_allocation_repository
    )
    app.dependency_overrides[get_record_repository] = lambda: mock_record_repository
    app.dependency_overrides[get_release_repository] = lambda: mock_release_repository

    with TestClient(app, base_url="http://testserver/api/v1") as c:
        yield c

    app.dependency_overrides = {}
