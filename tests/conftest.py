import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent.parent / ".env")

os.environ.setdefault("ASYNC_POOL_DISABLED", "1")
os.environ.setdefault("PSQL_HOST", "localhost")
os.environ.setdefault("PSQL_USER", "postgres")
os.environ.setdefault("PSQL_PASS", "postgres")
os.environ["PSQL_DB_NAME"] = os.environ.get("PSQL_TEST_DB_NAME", "dbm_nca_ph_test")
os.environ.setdefault("PIPELINE_API_KEY", "test-api-key-123")
os.environ.setdefault("SUPABASE_URL", "http://test.local")
os.environ.setdefault("SUPABASE_ANON_KEY", "test-anon-key")

import pytest
from fastapi.testclient import TestClient

from main import app
from src.presentation.api.dependencies import (
    get_allocation_repository,
    get_record_repository,
    get_release_repository,
)
from tests.mock.repositories.mock_allocation_repository import (
    MockAllocationRepository,
)
from tests.mock.repositories.mock_record_repository import MockRecordRepository
from tests.mock.repositories.mock_release_repository import (
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
