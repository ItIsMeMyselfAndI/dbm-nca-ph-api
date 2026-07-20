import pytest

from src.core.exceptions import NotFoundError
from src.core.use_cases.v2.pipeline.delete_allocation import DeleteAllocation


@pytest.fixture
def repo():
    from tests.mock.repositories_async.mock_async_allocation_repository import (
        MockAsyncAllocationRepository,
    )
    return MockAsyncAllocationRepository()


@pytest.fixture
def use_case(repo):
    return DeleteAllocation(repo)


@pytest.mark.asyncio
async def test_delete_allocation(use_case, repo):
    existing = repo.allocations[0]
    initial_count = len(repo.allocations)

    await use_case.execute(existing.id)

    assert len(repo.allocations) == initial_count - 1
    assert await repo.get_allocation_by_id(existing.id) is None


@pytest.mark.asyncio
async def test_delete_allocation_not_found(use_case):
    with pytest.raises(NotFoundError, match="Allocation with ID nonexistent not found"):
        await use_case.execute("nonexistent")
