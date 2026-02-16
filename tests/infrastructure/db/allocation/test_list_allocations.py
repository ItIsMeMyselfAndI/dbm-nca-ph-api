import pytest


@pytest.fixture
def repo():
    from tests.mock.repositories.mock_allocation_repository import (
        MockAllocationRepository,
    )

    return MockAllocationRepository()


def test_list_allocations(repo):
    allocations = repo.list_allocations(limit=10)
    assert len(allocations) == 10
    assert allocations[0].id == "00002e59-c77c-46b3-8068-f49e33f3674c"
    assert allocations[0].nca_number == "NCA-ROIVB-25-0000114"
    assert allocations[0].agency == ""
    assert allocations[0].operating_unit == "Coron School of Fisheries"
    assert allocations[0].amount == 13209000


def test_list_allocations_with_cursor(repo):
    first_page = repo.list_allocations(limit=5)
    assert len(first_page) == 5
    assert first_page[0].id == "00002e59-c77c-46b3-8068-f49e33f3674c"

    second_page = repo.list_allocations(limit=5, cursor=first_page[-1].id)
    assert len(second_page) == 5
    assert second_page[0].id == "00043fd2-c4dd-4890-8a55-63db6fce0eb6"


def test_list_allocations_with_invalid_cursor(repo):
    with pytest.raises(ValueError) as exc_info:
        repo.list_allocations(limit=5, cursor="nonexistent-id")
    assert str(exc_info.value) == "Cursor with ID nonexistent-id not found."


def test_list_allocations_with_empty_cursor(repo):
    allocations = repo.list_allocations(limit=5, cursor="")
    assert len(allocations) == 5


def test_list_allocations_with_none_cursor(repo):
    allocations = repo.list_allocations(limit=5, cursor=None)
    assert len(allocations) == 5


def test_list_allocations_with_leading_trailing_spaces_cursor(repo):
    with pytest.raises(ValueError) as exc_info:
        repo.list_allocations(limit=5, cursor=" 00002e59-c77c-46b3-8068-f49e33f3674c ")
    assert (
        str(exc_info.value)
        == "Cursor with ID  00002e59-c77c-46b3-8068-f49e33f3674c  not found."
    )


def test_list_allocations_with_case_sensitivity_cursor(repo):
    with pytest.raises(ValueError) as exc_info:
        repo.list_allocations(limit=5, cursor="00002E59-C77C-46B3-8068-F49E33F3674C")
    assert (
        str(exc_info.value)
        == "Cursor with ID 00002E59-C77C-46B3-8068-F49E33F3674C not found."
    )


def test_list_allocations_with_limit_zero(repo):
    allocations = repo.list_allocations(limit=0)
    assert len(allocations) == 0


def test_list_allocations_with_limit_exceeding_total(repo):
    allocations = repo.list_allocations(limit=100)
    assert len(allocations) == 40


# def test_list_allocations_with_negative_limit(repo):
#     allocations = repo.list_allocations(limit=-5)
#     assert len(allocations) == 0
