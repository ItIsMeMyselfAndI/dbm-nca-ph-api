import pytest

from src.core.use_cases.allocation.list_allocations import ListAllocations

ALLOCATION_ID = "0000a66b-0265-4b42-adfe-559f98646c91"
LIMIT_ROW_COUNT = 5


@pytest.fixture
def repo():
    from tests.mock.repositories.mock_allocation_repository import (
        MockAllocationRepository,
    )

    return MockAllocationRepository()


@pytest.fixture
def use_case(repo):
    from src.core.use_cases.allocation.list_allocations import ListAllocations

    return ListAllocations(repo)


def test_list_allocations(use_case: ListAllocations):
    allocations, next_cursor = use_case.execute(limit=LIMIT_ROW_COUNT)
    assert len(allocations) <= LIMIT_ROW_COUNT
    if len(allocations) != 0:
        assert next_cursor == allocations[-1].id


def test_list_allocations_with_cursor(use_case: ListAllocations):
    allocations, next_cursor = use_case.execute(
        limit=LIMIT_ROW_COUNT, cursor=ALLOCATION_ID
    )
    assert len(allocations) <= LIMIT_ROW_COUNT
    if len(allocations) != 0:
        assert next_cursor == allocations[-1].id


def test_list_allocations_with_invalid_cursor(use_case: ListAllocations):
    with pytest.raises(ValueError) as exc_info:
        use_case.execute(limit=LIMIT_ROW_COUNT, cursor="nonexistent-id")
    assert str(exc_info.value) == "Cursor with ID nonexistent-id not found."


def test_list_allocations_with_empty_cursor(use_case: ListAllocations):
    with pytest.raises(ValueError) as exc_info:
        use_case.execute(limit=LIMIT_ROW_COUNT, cursor="")
    assert str(exc_info.value) == "Cursor cannot be an empty string."


def test_list_allocations_with_leading_trailing_spaces_cursor(
    use_case: ListAllocations,
):
    allocations, next_cursor = use_case.execute(
        limit=LIMIT_ROW_COUNT, cursor=f" {ALLOCATION_ID} "
    )
    assert len(allocations) <= LIMIT_ROW_COUNT
    if len(allocations) != 0:
        assert next_cursor == allocations[-1].id


def test_list_allocations_with_upper_case_cursor(use_case: ListAllocations):
    allocations, next_cursor = use_case.execute(
        limit=LIMIT_ROW_COUNT, cursor=ALLOCATION_ID.upper()
    )
    assert len(allocations) <= LIMIT_ROW_COUNT
    if len(allocations) != 0:
        assert next_cursor == allocations[-1].id


def test_list_allocations_with_limit_zero(use_case: ListAllocations):
    allocations, next_cursor = use_case.execute(limit=0)
    assert len(allocations) == 0
    assert next_cursor is None


def test_list_allocations_with_negative_limit(use_case: ListAllocations):
    allocations, next_cursor = use_case.execute(limit=-5)
    assert len(allocations) == 0
    assert next_cursor is None
