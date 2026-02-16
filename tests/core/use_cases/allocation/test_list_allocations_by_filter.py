import pytest

from src.core.entities.allocation_filter import AllocationFilter


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


def test_list_allocations_by_filter(use_case):
    filter = {AllocationFilter.OPERATING_UNIT: "Coron School of Fisheries"}
    allocations, next_cursor = use_case.execute(filter=filter, limit=10)
    assert len(allocations) == 1
    assert next_cursor is None
    for allocation in allocations:
        assert allocation.operating_unit == "Coron School of Fisheries"


def test_list_allocations_by_filter_with_cursor(use_case):
    filter = {AllocationFilter.OPERATING_UNIT: "Coron School of Fisheries"}
    allocations, next_cursor = use_case.execute(filter=filter, limit=5)
    assert len(allocations) == 1
    assert next_cursor is None
    for allocation in allocations:
        assert allocation.operating_unit == "Coron School of Fisheries"

    # allocations_next, next_cursor_next = use_case.execute(
    #     filter=filter, limit=5, cursor=next_cursor
    # )
    # assert len(allocations_next) == 1
    # assert next_cursor_next is None
    # for allocation in allocations_next:
    #     assert allocation.operating_unit == "Coron School of Fisheries"


def test_list_allocations_by_filter_with_invalid_cursor(use_case):
    with pytest.raises(ValueError) as exc_info:
        filter = {AllocationFilter.OPERATING_UNIT: "Coron School of Fisheries"}
        use_case.execute(filter=filter, limit=5, cursor="nonexistent-id")
    assert str(exc_info.value) == "Cursor with ID nonexistent-id not found."


def test_list_allocations_by_filter_with_empty_cursor(use_case):
    with pytest.raises(ValueError) as exc_info:
        filter = {AllocationFilter.OPERATING_UNIT: "Coron School of Fisheries"}
        use_case.execute(filter=filter, limit=5, cursor="")
    assert str(exc_info.value) == "Cursor cannot be an empty string."


def test_list_allocations_by_filter_with_leading_trailing_spaces_cursor(use_case):
    filter = {AllocationFilter.OPERATING_UNIT: "Coron School of Fisheries"}
    allocations, next_cursor = use_case.execute(
        filter=filter,
        limit=5,
        cursor=" 00002e59-c77c-46b3-8068-f49e33f3674c ",
    )
    assert len(allocations) == 0
    assert next_cursor is None
    for allocation in allocations:
        assert allocation.operating_unit == "Coron School of Fisheries"


def test_list_allocations_by_filter_with_upper_case_cursor(use_case):
    filter = {AllocationFilter.OPERATING_UNIT: "Coron School of Fisheries"}
    allocations, next_cursor = use_case.execute(
        filter=filter,
        limit=5,
        cursor="00002E59-C77C-46B3-8068-F49E33F3674C",
    )
    assert len(allocations) == 0
    assert next_cursor is None


def test_list_allocations_by_filter_with_limit_zero(use_case):
    filter = {AllocationFilter.OPERATING_UNIT: "Coron School of Fisheries"}
    allocations, next_cursor = use_case.execute(filter=filter, limit=0)
    assert len(allocations) == 0
    assert next_cursor is None


def test_list_allocations_by_filter_with_limit_exceeding_total(use_case):
    filter = {AllocationFilter.OPERATING_UNIT: "Coron School of Fisheries"}
    allocations, next_cursor = use_case.execute(filter=filter, limit=100)
    assert len(allocations) == 1
    assert next_cursor is None


def test_list_allocations_by_filter_with_negative_limit(use_case):
    filter = {AllocationFilter.OPERATING_UNIT: "Coron School of Fisheries"}
    allocations, next_cursor = use_case.execute(filter=filter, limit=-5)
    assert len(allocations) == 0
    assert next_cursor is None


def test_list_allocations_by_filter_with_no_matching_records(use_case):
    filter = {AllocationFilter.OPERATING_UNIT: "Nonexistent Operating Unit"}
    allocations, next_cursor = use_case.execute(filter=filter, limit=10)
    assert len(allocations) == 0
    assert next_cursor is None
