import pytest
from fastapi.testclient import TestClient

from src.main import app
from src.presentation.api.dependencies import (
    get_allocation_repository,
    get_record_repository,
    get_release_repository,
)
from tests.infrastructure.db.mock_allocation_repository import MockAllocationRepository
from tests.infrastructure.db.mock_record_repository import MockRecordRepository
from tests.infrastructure.db.mock_release_repository import MockReleaseRepository


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
def client(mock_allocation_repo, mock_record_repo, mock_release_repo):
    app.dependency_overrides[get_allocation_repository] = lambda: mock_allocation_repo
    app.dependency_overrides[get_record_repository] = lambda: mock_record_repo
    app.dependency_overrides[get_release_repository] = lambda: mock_release_repo

    with TestClient(app) as c:
        yield c

    app.dependency_overrides = {}
