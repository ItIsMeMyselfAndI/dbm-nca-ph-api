import pytest

from src.core.entities.allocation_filter import AllocationFilter


@pytest.fixture
def repo():
    from tests.infrastructure.db.mock_allocation_repository import (
        MockAllocationRepository,
    )

    return MockAllocationRepository()


def test_list_allocations_by_filter(repo):
    filter = {AllocationFilter.OPERATING_UNIT: "Coron School of Fisheries"}
    allocations = repo.list_allocations_by_filter(limit=10, filter=filter)
    assert len(allocations) == 1
    for allocation in allocations:
        assert allocation.operating_unit == "Coron School of Fisheries"


def test_list_allocations_by_filter_with_cursor(repo):
    filter = {AllocationFilter.OPERATING_UNIT: "Coron School of Fisheries"}
    first_page = repo.list_allocations_by_filter(limit=5, filter=filter)
    assert len(first_page) == 1
    assert first_page[0].operating_unit == "Coron School of Fisheries"

    second_page = repo.list_allocations_by_filter(
        limit=5, filter=filter, cursor=first_page[-1].id
    )
    assert len(second_page) == 0
    # assert second_page[0].operating_unit == "Coron School of Fisheries"


def test_list_allocations_by_filter_with_invalid_cursor(repo):
    filter = {AllocationFilter.OPERATING_UNIT: "Coron School of Fisheries"}
    with pytest.raises(ValueError) as exc_info:
        repo.list_allocations_by_filter(limit=5, filter=filter, cursor="nonexistent-id")
    assert str(exc_info.value) == "Cursor with ID nonexistent-id not found."


def test_list_allocations_by_filter_with_empty_cursor(repo):
    filter = {AllocationFilter.OPERATING_UNIT: "Coron School of Fisheries"}
    with pytest.raises(ValueError) as exc_info:
        repo.list_allocations_by_filter(limit=5, filter=filter, cursor="")
    assert str(exc_info.value) == "Cursor with ID  not found."


def test_list_allocations_by_filter_with_none_cursor(repo):
    filter = {AllocationFilter.OPERATING_UNIT: "Coron School of Fisheries"}
    with pytest.raises(ValueError) as exc_info:
        repo.list_allocations_by_filter(limit=5, filter=filter, cursor=None)
    assert str(exc_info.value) == "Cursor with ID None not found."


def test_list_allocations_by_filter_with_leading_trailing_spaces_cursor(repo):
    filter = {AllocationFilter.OPERATING_UNIT: "Coron School of Fisheries"}
    with pytest.raises(ValueError) as exc_info:
        repo.list_allocations_by_filter(
            limit=5, filter=filter, cursor=" 00002e59-c77c-46b3-8068-f49e33f3674c "
        )
    assert (
        str(exc_info.value)
        == "Cursor with ID  00002e59-c77c-46b3-8068-f49e33f3674c  not found."
    )


def test_list_allocations_by_filter_with_case_sensitivity_cursor(repo):
    filter = {AllocationFilter.OPERATING_UNIT: "Coron School of Fisheries"}
    with pytest.raises(ValueError) as exc_info:
        repo.list_allocations_by_filter(
            limit=5, filter=filter, cursor="00002E59-C77C-46B3-8068-F49E33F3674C"
        )
    assert (
        str(exc_info.value)
        == "Cursor with ID 00002E59-C77C-46B3-8068-F49E33F3674C not found."
    )


def test_list_allocations_by_filter_with_limit_zero(repo):
    filter = {AllocationFilter.OPERATING_UNIT: "Coron School of Fisheries"}
    allocations = repo.list_allocations_by_filter(limit=0, filter=filter)
    assert len(allocations) == 0


def test_list_allocations_by_filter_with_limit_exceeding_total(repo):
    filter = {AllocationFilter.OPERATING_UNIT: "Coron School of Fisheries"}
    allocations = repo.list_allocations_by_filter(limit=100, filter=filter)
    assert len(allocations) == 1


def test_list_allocations_by_filter_with_negative_limit(repo):
    filter = {AllocationFilter.OPERATING_UNIT: "Coron School of Fisheries"}
    with pytest.raises(ValueError) as exc_info:
        repo.list_allocations_by_filter(limit=-5, filter=filter)
    assert str(exc_info.value) == "Limit must be a non-negative integer."


def test_list_allocations_by_filter_with_no_matching_records(repo):
    filter = {AllocationFilter.OPERATING_UNIT: "Nonexistent Operating Unit"}
    allocations = repo.list_allocations_by_filter(limit=10, filter=filter)
    assert len(allocations) == 0
