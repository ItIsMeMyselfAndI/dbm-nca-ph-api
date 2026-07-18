import pytest

from src.core.entities.allocation_filter import AllocationFilter
from src.core.exceptions import ValidationError

ALLOCATION_ID = "0000a66b-0265-4b42-adfe-559f98646c91"
ALLOCATION_FILTER_KEY = AllocationFilter.OPERATING_UNIT
ALLOCATION_FILTER_VALUE = "Central Office"
FILTER = {ALLOCATION_FILTER_KEY: ALLOCATION_FILTER_VALUE}


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


@pytest.mark.asyncio
async def test_list_allocations_by_filter_with_cursor(use_case):
    allocations, next_cursor = await use_case.execute(limit=10, filter=FILTER)
    assert len(allocations) <= 10
    if allocations:
        assert next_cursor == allocations[-1].id
    for allocation in allocations:
        assert allocation.operating_unit == ALLOCATION_FILTER_VALUE

    allocations_next, next_cursor_next = await use_case.execute(
        limit=10, filter=FILTER, cursor=next_cursor
    )
    assert len(allocations_next) <= 10
    if allocations_next:
        assert next_cursor_next == allocations_next[-1].id
    for allocation in allocations_next:
        assert allocation.operating_unit == ALLOCATION_FILTER_VALUE


@pytest.mark.asyncio
async def test_list_allocations_by_filter_with_invalid_cursor(use_case):
    allocations, next_cursor = await use_case.execute(
        limit=10, filter=FILTER, cursor="nonexistent-id"
    )
    assert len(allocations) == 0
    assert next_cursor is None


@pytest.mark.asyncio
async def test_list_allocations_by_filter_with_leading_trailing_spaces_cursor(use_case):
    allocations, next_cursor = await use_case.execute(
        limit=10, filter=FILTER, cursor=f" {ALLOCATION_ID} "
    )
    assert len(allocations) <= 10
    if allocations:
        assert next_cursor == allocations[-1].id
    for allocation in allocations:
        assert allocation.operating_unit == ALLOCATION_FILTER_VALUE


@pytest.mark.asyncio
async def test_list_allocations_by_filter_with_upper_case_cursor(use_case):
    allocations, next_cursor = await use_case.execute(
        limit=10, filter=FILTER, cursor=ALLOCATION_ID.upper()
    )
    assert len(allocations) <= 10
    if allocations:
        assert next_cursor == allocations[-1].id
    for allocation in allocations:
        assert allocation.operating_unit == ALLOCATION_FILTER_VALUE


@pytest.mark.asyncio
async def test_list_allocations_by_filter_with_negative_limit(use_case):
    allocations, next_cursor = await use_case.execute(
        limit=-5, filter=FILTER,
    )
    assert len(allocations) == 0
    assert next_cursor is None


@pytest.mark.asyncio
async def test_list_allocations_by_filter_with_no_matching_records(use_case):
    allocations, next_cursor = await use_case.execute(
        limit=10,
        filter={ALLOCATION_FILTER_KEY: "Nonexistent Operating Unit"},
    )
    assert len(allocations) == 0
    assert next_cursor is None
