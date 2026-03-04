import pytest

from src.core.use_cases.allocation.get_allocation_by_id import GetAllocationByID

ALLOCATION_ID = "00094280-64b6-43c7-893a-a0c18d73834a"


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


def test_get_allocation_by_id(use_case: GetAllocationByID):
    allocation = use_case.execute(ALLOCATION_ID)
    assert allocation.id == ALLOCATION_ID


def test_get_allocation_by_id_not_found(use_case: GetAllocationByID):
    with pytest.raises(ValueError) as exc_info:
        use_case.execute("nonexistent-id")
    assert str(exc_info.value) == "Allocation with ID nonexistent-id not found."


def test_get_allocation_by_id_empty_string(use_case: GetAllocationByID):
    with pytest.raises(ValueError) as exc_info:
        use_case.execute("")
    assert str(exc_info.value) == "Allocation with ID  not found."


def test_get_allocation_by_id_in_upper_case(use_case: GetAllocationByID):
    allocation = use_case.execute(ALLOCATION_ID.upper())
    assert allocation.id == ALLOCATION_ID


def test_get_allocation_by_id_leading_trailing_spaces(use_case: GetAllocationByID):
    allocation = use_case.execute(f" {ALLOCATION_ID} ")
    assert allocation.id == ALLOCATION_ID
