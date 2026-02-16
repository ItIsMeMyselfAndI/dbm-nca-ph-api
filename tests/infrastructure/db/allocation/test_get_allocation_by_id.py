import pytest


@pytest.fixture
def repo():
    from tests.mock.repositories.mock_allocation_repository import (
        MockAllocationRepository,
    )

    return MockAllocationRepository()


def test_get_allocation_by_id(repo):
    allocation = repo.get_allocation_by_id("00002e59-c77c-46b3-8068-f49e33f3674c")
    assert allocation.id == "00002e59-c77c-46b3-8068-f49e33f3674c"


def test_get_allocation_by_id_not_found(repo):
    with pytest.raises(ValueError) as exc_info:
        repo.get_allocation_by_id("nonexistent-id")
    assert str(exc_info.value) == "Allocation with ID nonexistent-id not found."


def test_get_allocation_by_id_empty_string(repo):
    with pytest.raises(ValueError) as exc_info:
        repo.get_allocation_by_id("")
    assert str(exc_info.value) == "Allocation with ID  not found."


# def test_get_allocation_by_id_none(repo):
#     with pytest.raises(ValueError) as exc_info:
#         repo.get_allocation_by_id(None)
#     assert str(exc_info.value) == "Allocation with ID None not found."
#
#
def test_get_allocation_by_id_in_upper_case(repo):
    allocation = repo.get_allocation_by_id("00002E59-C77C-46B3-8068-F49E33F3674C")
    assert allocation.id == "00002e59-c77c-46b3-8068-f49e33f3674c"


def test_get_allocation_by_id_leading_trailing_spaces(repo):
    allocation = repo.get_allocation_by_id(" 00002e59-c77c-46b3-8068-f49e33f3674c ")
    assert allocation.id == "00002e59-c77c-46b3-8068-f49e33f3674c"
