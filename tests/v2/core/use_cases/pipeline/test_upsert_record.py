import pytest

from src.core.entities.record import Record
from src.core.use_cases.v2.pipeline.upsert_record import UpsertRecord


@pytest.fixture
def repo():
    from tests.mock.repositories_async.mock_async_record_repository import (
        MockAsyncRecordRepository,
    )
    return MockAsyncRecordRepository()


@pytest.fixture
def use_case(repo):
    return UpsertRecord(repo)


@pytest.mark.asyncio
async def test_upsert_record_create(use_case, repo):
    initial_count = len(repo.records)
    new_record = Record(
        id="new-uuid-for-test",
        nca_number="NCA-TEST-99-0000001",
        nca_type="REG",
        released_date="2024-01-01T00:00:00+00:00",
        department="Test Department",
        purpose="Test purpose",
        release_id="id_2024",
    )
    result, was_created = await use_case.execute(new_record)
    assert result.nca_number == "NCA-TEST-99-0000001"
    assert was_created is True
    assert len(repo.records) == initial_count + 1


@pytest.mark.asyncio
async def test_upsert_record_update(use_case, repo):
    initial_count = len(repo.records)
    existing_nca = repo.records[0].nca_number
    existing_id = repo.records[0].id
    updated_record = Record(
        id="new-uuid",
        nca_number=existing_nca,
        nca_type="REG",
        released_date="2025-01-01T00:00:00+00:00",
        department="Updated Department",
        purpose="Updated purpose",
        release_id="id_2025",
    )
    result, was_created = await use_case.execute(updated_record)
    assert result.nca_number == existing_nca
    assert was_created is False
    updated_in_repo = await repo.get_record_by_id(existing_id)
    assert updated_in_repo is not None
    assert updated_in_repo.department == "Updated Department"
    assert len(repo.records) == initial_count


@pytest.mark.asyncio
async def test_upsert_record_update_all_fields(use_case, repo):
    existing_nca = repo.records[1].nca_number
    existing_id = repo.records[1].id
    updated = Record(
        id="uuid-another",
        nca_number=existing_nca,
        nca_type="REG",
        released_date="2026-06-06T00:00:00+00:00",
        department="New Dept",
        purpose="New purpose",
        release_id="id_2026",
    )
    result, was_created = await use_case.execute(updated)
    assert result.released_date == "2026-06-06T00:00:00+00:00"
    assert result.department == "New Dept"
    assert result.purpose == "New purpose"
    assert result.release_id == "id_2026"
    assert was_created is False
    record = await repo.get_record_by_id(existing_id)
    assert record is not None
    assert record.released_date == "2026-06-06T00:00:00+00:00"


@pytest.mark.asyncio
async def test_upsert_record_multiple_nca_calls(use_case, repo):
    nca_number = "NCA-MULTI-99-0000999"
    record1 = Record(
        id="uuid-1",
        nca_number=nca_number,
        nca_type="REG",
        released_date="2024-01-01T00:00:00+00:00",
        department="First",
        purpose="First purpose",
        release_id="id_2024",
    )
    result1, was_created1 = await use_case.execute(record1)
    assert result1.nca_number == nca_number
    assert was_created1 is True

    record2 = Record(
        id="uuid-2",
        nca_number=nca_number,
        nca_type="REG",
        released_date="2025-01-01T00:00:00+00:00",
        department="Second",
        purpose="Second purpose",
        release_id="id_2025",
    )
    result2, was_created2 = await use_case.execute(record2)
    assert result2.department == "Second"
    assert was_created2 is False
    assert len([r for r in repo.records if r.nca_number == nca_number]) == 1
