import pytest

from src.core.entities.allocation_filter import AllocationFilter
from src.core.exceptions import ValidationError


@pytest.fixture
def repo():
    from tests.mock.repositories_async.mock_async_allocation_repository import (
        MockAsyncAllocationRepository,
    )
    return MockAsyncAllocationRepository()


@pytest.fixture
def use_case(repo):
    from src.core.use_cases.v2.allocation.list_allocations_by_filter import (
        ListAllocationsByFilter,
    )
    return ListAllocationsByFilter(repo)


@pytest.mark.asyncio
async def test_list_allocations_by_filter(use_case):
    allocations, next_cursor = await use_case.execute(
        limit=10,
        filter={AllocationFilter.NCA_NUMBER: "NCA-NCR-25-0001001"},
    )
    assert len(allocations) <= 10
    if allocations:
        assert next_cursor == allocations[-1].id


@pytest.mark.asyncio
async def test_list_allocations_by_filter_empty_cursor(use_case):
    with pytest.raises(ValidationError, match="Cursor cannot be an empty string."):
        await use_case.execute(
            limit=10,
            filter={AllocationFilter.NCA_NUMBER: "NCA-NCR-25-0001001"},
            cursor="",
        )


@pytest.mark.asyncio
async def test_list_allocations_by_filter_limit_zero(use_case):
    allocations, next_cursor = await use_case.execute(
        limit=0,
        filter={AllocationFilter.NCA_NUMBER: "NCA-NCR-25-0001001"},
    )
    assert len(allocations) == 0
    assert next_cursor is None
