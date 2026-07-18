import pytest

from src.core.entities.allocation_filter import AllocationFilter


@pytest.fixture
def repo():
    from tests.mock.repositories.mock_allocation_repository import (
        MockAllocationRepository,
    )

    return MockAllocationRepository()


FILTER = {AllocationFilter.OPERATING_UNIT: "Engr. Virgilio V. Dionisio Memorial School"}


def test_list_allocations_by_filter(repo):
    allocations = repo.list_allocations_by_filter(limit=10, filter=FILTER)
    assert len(allocations) == 1
    for allocation in allocations:
        assert allocation.operating_unit == "Engr. Virgilio V. Dionisio Memorial School"


def test_list_allocations_by_filter_with_cursor(repo):
    first_page = repo.list_allocations_by_filter(limit=5, filter=FILTER)
    assert len(first_page) == 1

    second_page = repo.list_allocations_by_filter(
        limit=5, filter=FILTER, cursor=first_page[-1].id
    )
    assert len(second_page) == 0


def test_list_allocations_by_filter_by_agency(repo):
    filter = {AllocationFilter.AGENCY: "Foreign Service Institute"}
    allocations = repo.list_allocations_by_filter(limit=10, filter=filter)
    assert len(allocations) == 1
    assert allocations[0].agency == "Foreign Service Institute"


def test_list_allocations_by_filter_by_nca_number(repo):
    filter = {AllocationFilter.NCA_NUMBER: "NCA-ROVII-24-0007482"}
    allocations = repo.list_allocations_by_filter(limit=10, filter=filter)
    assert len(allocations) == 4
    for allocation in allocations:
        assert allocation.nca_number == "NCA-ROVII-24-0007482"


def test_list_allocations_by_filter_by_nca_number_with_cursor(repo):
    filter = {AllocationFilter.NCA_NUMBER: "NCA-ROVII-24-0007482"}
    first_page = repo.list_allocations_by_filter(limit=2, filter=filter)
    assert len(first_page) == 2

    second_page = repo.list_allocations_by_filter(
        limit=2, filter=filter, cursor=first_page[-1].id
    )
    assert len(second_page) == 2

    third_page = repo.list_allocations_by_filter(
        limit=2, filter=filter, cursor=second_page[-1].id
    )
    assert len(third_page) == 0


def test_list_allocations_by_filter_with_invalid_cursor(repo):
    with pytest.raises(ValueError) as exc_info:
        repo.list_allocations_by_filter(limit=5, filter=FILTER, cursor="nonexistent-id")
    assert str(exc_info.value) == "Cursor with ID nonexistent-id not found."


def test_list_allocations_by_filter_with_empty_cursor(repo):
    allocations = repo.list_allocations_by_filter(limit=5, filter=FILTER, cursor="")
    assert len(allocations) == 1
    for allocation in allocations:
        assert allocation.operating_unit == "Engr. Virgilio V. Dionisio Memorial School"


def test_list_allocations_by_filter_with_none_cursor(repo):
    allocations = repo.list_allocations_by_filter(limit=5, filter=FILTER, cursor=None)
    assert len(allocations) == 1
    for allocation in allocations:
        assert allocation.operating_unit == "Engr. Virgilio V. Dionisio Memorial School"


def test_list_allocations_by_filter_with_leading_trailing_spaces_cursor(repo):
    allocations = repo.list_allocations_by_filter(
        limit=5, filter=FILTER, cursor=" 0318b06b-d007-4f40-a257-ae98a9036609 "
    )
    assert len(allocations) == 0
    for allocation in allocations:
        assert allocation.operating_unit == "Engr. Virgilio V. Dionisio Memorial School"


def test_list_allocations_by_filter_with_upper_case_cursor(repo):
    allocations = repo.list_allocations_by_filter(
        limit=5, filter=FILTER, cursor="0318B06B-D007-4F40-A257-AE98A9036609"
    )
    assert len(allocations) == 0
    for allocation in allocations:
        assert allocation.operating_unit == "Engr. Virgilio V. Dionisio Memorial School"


def test_list_allocations_by_filter_with_limit_zero(repo):
    allocations = repo.list_allocations_by_filter(limit=0, filter=FILTER)
    assert len(allocations) == 0


def test_list_allocations_by_filter_with_limit_exceeding_total(repo):
    allocations = repo.list_allocations_by_filter(limit=100, filter=FILTER)
    assert len(allocations) == 1


def test_list_allocations_by_filter_with_negative_limit(repo):
    allocations = repo.list_allocations_by_filter(limit=-5, filter=FILTER)
    assert len(allocations) == 0


def test_list_allocations_by_filter_with_no_matching_records(repo):
    filter = {AllocationFilter.OPERATING_UNIT: "Nonexistent Operating Unit"}
    allocations = repo.list_allocations_by_filter(limit=10, filter=filter)
    assert len(allocations) == 0
