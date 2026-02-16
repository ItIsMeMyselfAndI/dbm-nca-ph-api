import pytest


@pytest.fixture
def repo():
    from tests.mock.repositories.mock_allocation_repository import (
        MockAllocationRepository,
    )

    return MockAllocationRepository()


@pytest.fixture
def use_case(repo):
    from src.core.use_cases.allocation.get_allocation_by_id import GetAllocationByID

    return GetAllocationByID(repo)


def test_get_allocation_by_id(use_case):
    allocation = use_case.execute("00002e59-c77c-46b3-8068-f49e33f3674c")
    assert allocation.id == "00002e59-c77c-46b3-8068-f49e33f3674c"
    assert allocation.nca_number == "NCA-ROIVB-25-0000114"
    assert allocation.agency == ""
    assert allocation.operating_unit == "Coron School of Fisheries"
    assert allocation.amount == 13209000


def test_get_allocation_by_id_not_found(use_case):
    with pytest.raises(ValueError) as exc_info:
        use_case.execute("nonexistent-id")
    assert str(exc_info.value) == "Allocation with ID nonexistent-id not found."


def test_get_allocation_by_id_empty_string(use_case):
    with pytest.raises(ValueError) as exc_info:
        use_case.execute("")
    assert str(exc_info.value) == "Allocation with ID  not found."


def test_get_allocation_by_id_case_sensitivity(use_case):
    with pytest.raises(ValueError) as exc_info:
        use_case.execute("00002E59-C77C-46B3-8068-F49E33F3674C")
    assert (
        str(exc_info.value)
        == "Allocation with ID 00002E59-C77C-46B3-8068-F49E33F3674C not found."
    )


def test_get_allocation_by_id_leading_trailing_spaces(use_case):
    with pytest.raises(ValueError) as exc_info:
        use_case.execute(" 00002e59-c77c-46b3-8068-f49e33f3674c ")
    assert (
        str(exc_info.value)
        == "Allocation with ID  00002e59-c77c-46b3-8068-f49e33f3674c  not found."
    )
