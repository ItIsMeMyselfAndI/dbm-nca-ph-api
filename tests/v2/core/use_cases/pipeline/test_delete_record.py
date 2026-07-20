import pytest

from src.core.exceptions import NotFoundError
from src.core.use_cases.v2.pipeline.delete_record import DeleteRecord
from src.core.entities.record_filter import RecordFilter


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
def use_case(record_repo, allocation_repo):
    return DeleteRecord(record_repo, allocation_repo)


@pytest.mark.asyncio
async def test_delete_record(use_case, record_repo):
    existing = record_repo.records[0]
    initial_count = len(record_repo.records)

    await use_case.execute(existing.nca_number)

    assert len(record_repo.records) == initial_count - 1
    assert await record_repo.get_record_by_id(existing.id) is None


@pytest.mark.asyncio
async def test_delete_record_not_found(use_case):
    with pytest.raises(NotFoundError, match="Record with ID NCA-NONEXISTENT not found"):
        await use_case.execute("NCA-NONEXISTENT")


@pytest.mark.asyncio
async def test_delete_record_with_multiple_matching_filter(use_case, record_repo):
    existing = record_repo.records[0]
    initial_count = len(record_repo.records)

    await use_case.execute(existing.nca_number)

    remaining = await record_repo.list_records_by_filter(
        limit=10, filter={RecordFilter.NCA_NUMBER: existing.nca_number}
    )
    assert len(remaining) == 0
    assert len(record_repo.records) == initial_count - 1
