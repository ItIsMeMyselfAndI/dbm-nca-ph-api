import pytest

from src.core.entities.allocation import Allocation
from src.core.use_cases.v2.pipeline.upsert_allocation import UpsertAllocation


@pytest.fixture
def repo():
    from tests.mock.repositories_async.mock_async_allocation_repository import (
        MockAsyncAllocationRepository,
    )
    return MockAsyncAllocationRepository()


@pytest.fixture
def use_case(repo):
    return UpsertAllocation(repo)


@pytest.mark.asyncio
async def test_upsert_allocation_create(use_case, repo):
    initial_count = len(repo.allocations)
    new_allocation = Allocation(
        id="new-uuid-alloc",
        nca_number="NCA-TEST-99-0000001",
        agency="Test Agency",
        operating_unit="Test OU",
        amount=50000.0,
    )
    result = await use_case.execute(new_allocation)
    assert result.nca_number == "NCA-TEST-99-0000001"
    assert result.agency == "Test Agency"
    assert result.operating_unit == "Test OU"
    assert result.amount == 50000.0
    assert len(repo.allocations) == initial_count + 1


@pytest.mark.asyncio
async def test_upsert_allocation_update(use_case, repo):
    existing = repo.allocations[0]
    initial_count = len(repo.allocations)
    updated_allocation = Allocation(
        id="new-uuid-alloc-upd",
        nca_number=existing.nca_number,
        agency=existing.agency,
        operating_unit=existing.operating_unit,
        amount=999999.0,
    )
    result = await use_case.execute(updated_allocation)
    assert result.nca_number == existing.nca_number
    assert result.amount == 999999.0
    assert len(repo.allocations) == initial_count
    fetched = await repo.get_allocation_by_id(result.id)
    assert fetched is not None
    assert fetched.amount == 999999.0


@pytest.mark.asyncio
async def test_upsert_allocation_same_nca_diff_agency(use_case, repo):
    nca = repo.allocations[0].nca_number
    existing_agency = repo.allocations[0].agency
    existing_ou = repo.allocations[0].operating_unit
    initial_count = len(repo.allocations)

    diff_agency = Allocation(
        id="uuid-diff-agency",
        nca_number=nca,
        agency="Different Agency",
        operating_unit=existing_ou,
        amount=1000.0,
    )
    result = await use_case.execute(diff_agency)
    assert result.agency == "Different Agency"
    assert len(repo.allocations) == initial_count + 1


@pytest.mark.asyncio
async def test_upsert_allocation_same_nca_diff_ou(use_case, repo):
    nca = repo.allocations[0].nca_number
    existing_agency = repo.allocations[0].agency
    initial_count = len(repo.allocations)

    diff_ou = Allocation(
        id="uuid-diff-ou",
        nca_number=nca,
        agency=existing_agency,
        operating_unit="Different OU",
        amount=2000.0,
    )
    result = await use_case.execute(diff_ou)
    assert result.operating_unit == "Different OU"
    assert len(repo.allocations) == initial_count + 1


@pytest.mark.asyncio
async def test_upsert_allocation_update_same_composite_key(use_case, repo):
    for a in repo.allocations:
        if a.agency and a.operating_unit and a.nca_number:
            target = a
            break
    else:
        pytest.skip("No allocation with all fields populated")

    initial_count = len(repo.allocations)
    updated = Allocation(
        id="uuid-update-composite",
        nca_number=target.nca_number,
        agency=target.agency,
        operating_unit=target.operating_unit,
        amount=777777.0,
    )
    result = await use_case.execute(updated)
    assert result.amount == 777777.0
    assert len(repo.allocations) == initial_count
