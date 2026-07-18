import pytest

from src.core.exceptions import ValidationError


@pytest.fixture
def repo():
    from tests.mock.repositories_async.mock_async_allocation_repository import (
        MockAsyncAllocationRepository,
    )
    return MockAsyncAllocationRepository()


@pytest.fixture
def use_case(repo):
    from src.core.use_cases.v2.allocation.list_allocations import ListAllocations
    return ListAllocations(repo)


@pytest.mark.asyncio
async def test_list_allocations(use_case):
    allocations, next_cursor = await use_case.execute(limit=10)
    assert len(allocations) <= 10
    if allocations:
        assert next_cursor == allocations[-1].id


@pytest.mark.asyncio
async def test_list_allocations_with_cursor(use_case):
    allocations, next_cursor = await use_case.execute(limit=5)
    next_cursor_val = next_cursor
    allocations_next, next_cursor_next = await use_case.execute(limit=5, cursor=next_cursor_val)
    assert len(allocations_next) <= 5
    if allocations_next:
        assert next_cursor_next == allocations_next[-1].id


@pytest.mark.asyncio
async def test_list_allocations_with_empty_cursor(use_case):
    with pytest.raises(ValidationError, match="Cursor cannot be an empty string."):
        await use_case.execute(limit=5, cursor="")


@pytest.mark.asyncio
async def test_list_allocations_with_limit_zero(use_case):
    allocations, next_cursor = await use_case.execute(limit=0)
    assert len(allocations) == 0
    assert next_cursor is None


@pytest.mark.asyncio
async def test_list_allocations_with_negative_limit(use_case):
    allocations, next_cursor = await use_case.execute(limit=-5)
    assert len(allocations) == 0
    assert next_cursor is None
