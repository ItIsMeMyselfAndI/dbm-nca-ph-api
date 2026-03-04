import pytest

from src.core.entities.allocation_filter import AllocationFilter
from src.core.use_cases.allocation.list_allocations_by_filter import (
    ListAllocationsByFilter,
)

ALLOCATION_ID = "00094280-64b6-43c7-893a-a0c18d73834a"
ALLOCATION_FILTER_KEY = AllocationFilter.OPERATING_UNIT
ALLOCATION_FILTER_VALUE = "Central Office"
FILTER = {ALLOCATION_FILTER_KEY: ALLOCATION_FILTER_VALUE}
LIMIT_ROW_COUNT = 10


@pytest.fixture
def repo():
    from tests.mock.repositories.mock_allocation_repository import (
        MockAllocationRepository,
    )

    return MockAllocationRepository()


@pytest.fixture
def use_case(repo):
    from src.core.use_cases.allocation.list_allocations_by_filter import (
        ListAllocationsByFilter,
    )

    return ListAllocationsByFilter(repo)


def test_list_allocations_by_filter(use_case: ListAllocationsByFilter):
    allocations, next_cursor = use_case.execute(filter=FILTER, limit=LIMIT_ROW_COUNT)
    assert len(allocations) <= LIMIT_ROW_COUNT
    if len(allocations) != 0:
        assert next_cursor == allocations[-1].id
    for allocation in allocations:
        assert allocation.operating_unit == ALLOCATION_FILTER_VALUE


def test_list_allocations_by_filter_with_cursor(use_case: ListAllocationsByFilter):
    allocations, next_cursor = use_case.execute(filter=FILTER, limit=LIMIT_ROW_COUNT)
    assert len(allocations) <= LIMIT_ROW_COUNT
    if len(allocations) != 0:
        assert next_cursor == allocations[-1].id
    for allocation in allocations:
        assert allocation.operating_unit == ALLOCATION_FILTER_VALUE

    allocations_next, next_cursor_next = use_case.execute(
        filter=FILTER, limit=LIMIT_ROW_COUNT, cursor=next_cursor
    )
    assert len(allocations_next) <= LIMIT_ROW_COUNT
    if len(allocations_next) != 0:
        assert next_cursor_next == allocations_next[-1].id
    for allocation in allocations_next:
        assert allocation.operating_unit == ALLOCATION_FILTER_VALUE


def test_list_allocations_by_filter_with_invalid_cursor(
    use_case: ListAllocationsByFilter,
):
    with pytest.raises(ValueError) as exc_info:
        use_case.execute(filter=FILTER, limit=LIMIT_ROW_COUNT, cursor="nonexistent-id")
    assert str(exc_info.value) == "Cursor with ID nonexistent-id not found."


def test_list_allocations_by_filter_with_empty_cursor(
    use_case: ListAllocationsByFilter,
):
    with pytest.raises(ValueError) as exc_info:
        use_case.execute(filter=FILTER, limit=LIMIT_ROW_COUNT, cursor="")
    assert str(exc_info.value) == "Cursor cannot be an empty string."


def test_list_allocations_by_filter_with_leading_trailing_spaces_cursor(
    use_case: ListAllocationsByFilter,
):
    allocations, next_cursor = use_case.execute(
        filter=FILTER,
        limit=LIMIT_ROW_COUNT,
        cursor=f" {ALLOCATION_ID} ",
    )
    assert len(allocations) <= LIMIT_ROW_COUNT
    if len(allocations) != 0:
        assert next_cursor == allocations[-1].id
    for allocation in allocations:
        assert allocation.operating_unit == ALLOCATION_FILTER_VALUE


def test_list_allocations_by_filter_with_upper_case_cursor(
    use_case: ListAllocationsByFilter,
):
    allocations, next_cursor = use_case.execute(
        filter=FILTER,
        limit=LIMIT_ROW_COUNT,
        cursor=ALLOCATION_ID.upper(),
    )
    assert len(allocations) <= LIMIT_ROW_COUNT
    if len(allocations) != 0:
        assert next_cursor == allocations[-1].id
    for allocation in allocations:
        assert allocation.operating_unit == ALLOCATION_FILTER_VALUE


def test_list_allocations_by_filter_with_limit_zero(use_case: ListAllocationsByFilter):
    allocations, next_cursor = use_case.execute(filter=FILTER, limit=0)
    assert len(allocations) == 0
    assert next_cursor is None


def test_list_allocations_by_filter_with_negative_limit(
    use_case: ListAllocationsByFilter,
):
    allocations, next_cursor = use_case.execute(filter=FILTER, limit=-5)
    assert len(allocations) == 0
    assert next_cursor is None


def test_list_allocations_by_filter_with_no_matching_records(
    use_case: ListAllocationsByFilter,
):
    allocations, next_cursor = use_case.execute(
        filter={ALLOCATION_FILTER_KEY: "Nonexistent Operating Unit"},
        limit=LIMIT_ROW_COUNT,
    )
    assert len(allocations) == 0
    assert next_cursor is None
