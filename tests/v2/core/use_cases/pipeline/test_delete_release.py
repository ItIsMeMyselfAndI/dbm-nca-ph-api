import pytest

from src.core.exceptions import NotFoundError
from src.core.use_cases.v2.pipeline.delete_release import DeleteRelease


@pytest.fixture
def release_repo():
    from tests.mock.repositories_async.mock_async_release_repository import (
        MockAsyncReleaseRepository,
    )
    return MockAsyncReleaseRepository()


@pytest.fixture
def record_repo():
    from tests.mock.repositories_async.mock_async_record_repository import (
        MockAsyncRecordRepository,
    )
    return MockAsyncRecordRepository()


@pytest.fixture
def allocation_repo():
    from tests.mock.repositories_async.mock_async_allocation_repository import (
        MockAsyncAllocationRepository,
    )
    return MockAsyncAllocationRepository()


@pytest.fixture
def use_case(release_repo, record_repo, allocation_repo):
    return DeleteRelease(release_repo, record_repo, allocation_repo)


@pytest.mark.asyncio
async def test_delete_release(use_case, release_repo, record_repo):
    initial_release_count = len(release_repo.releases)
    records_for_release = [r for r in record_repo.records if r.release_id == "id_2024"]
    initial_record_count = len(record_repo.records)

    await use_case.execute("id_2024")

    assert len(release_repo.releases) == initial_release_count - 1
    assert len(record_repo.records) == initial_record_count - len(records_for_release)
    assert release_repo.get_release_by_id("id_2024") is None
    for r in records_for_release:
        assert record_repo.get_record_by_id(r.id) is None


@pytest.mark.asyncio
async def test_delete_release_not_found(use_case):
    with pytest.raises(NotFoundError, match="Release with ID nonexistent not found"):
        await use_case.execute("nonexistent")


@pytest.mark.asyncio
async def test_delete_release_no_associated_records(use_case, release_repo):
    new_release = type("Release", (), {
        "id": "orphan-release",
        "title": "",
        "url": "",
        "filename": "",
        "year": 2026,
        "page_count": 0,
    })()
    await release_repo.create_release(new_release)
    initial_count = len(release_repo.releases)

    await use_case.execute("orphan-release")

    assert len(release_repo.releases) == initial_count - 1
