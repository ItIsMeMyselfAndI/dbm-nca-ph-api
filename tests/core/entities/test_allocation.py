import pytest
from src.core.entities.allocation import Allocation


def test_allocation():
    allocation = Allocation(
        id="123",
        nca_number="NCA-456",
        agency="Agency A",
        operating_unit="Unit 1",
        amount=1000.0,
    )

    assert allocation.id == "123"
    assert allocation.nca_number == "NCA-456"
    assert allocation.agency == "Agency A"
    assert allocation.operating_unit == "Unit 1"
    assert allocation.amount == 1000.0


def test_allocation_missing_fields():
    with pytest.raises(ValueError) as exc_info:
        allocation = Allocation(  # pyright: ignore
            id="126",
            nca_number="NCA-102",
            agency="Agency D",
            amount=2000.0,
        )
    print(exc_info.value)


def test_allocation_non_string_id():
    with pytest.raises(ValueError) as exc_info:
        allocation = Allocation(
            id=123,  # pyright: ignore
            nca_number="NCA-107",
            agency="Agency H",
            operating_unit="Unit 8",
            amount=300.0,
        )
    print(exc_info.value)


def test_allocation_non_string_nca_number():
    with pytest.raises(ValueError) as exc_info:
        allocation = Allocation(
            id="131",
            nca_number=456,  # pyright: ignore
            agency="Agency I",
            operating_unit="Unit 9",
            amount=400.0,
        )
    print(exc_info.value)


def test_allocation_non_string_agency():
    with pytest.raises(ValueError) as exc_info:
        allocation = Allocation(
            id="132",
            nca_number="NCA-108",
            agency=789,  # pyright: ignore
            operating_unit="Unit 10",
            amount=600.0,
        )
    print(exc_info.value)


def test_allocation_non_string_operating_unit():
    with pytest.raises(ValueError) as exc_info:
        allocation = Allocation(
            id="133",
            nca_number="NCA-109",
            agency="Agency J",
            operating_unit=101,  # pyright: ignore
            amount=700.0,
        )
    print(exc_info.value)


def test_allocation_non_numeric_amount():
    with pytest.raises(ValueError) as exc_info:
        allocation = Allocation(
            id="134",
            nca_number="NCA-110",
            agency="Agency K",
            operating_unit="Unit 11",
            amount="eight hundred",  # pyright: ignore
        )
    print(exc_info.value)
