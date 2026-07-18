import pytest

from src.core.entities.record_filter import RecordFilter
from src.core.exceptions import ValidationError

RECORD_ID = "a729caee-c88f-416b-ba35-fca60a553aaa"
RECORD_FILTER_KEY = RecordFilter.DEPARTMENT
RECORD_FILTER_VALUE = "Department of Education (DepEd)"
FILTER = {RECORD_FILTER_KEY: RECORD_FILTER_VALUE}


@pytest.fixture
def repo():
    from tests.mock.repositories_async.mock_async_record_repository import (
        MockAsyncRecordRepository,
    )
    return MockAsyncRecordRepository()


@pytest.fixture
def use_case(repo):
    from src.core.use_cases.v2.record.list_records_by_filter import ListRecordsByFilter
    return ListRecordsByFilter(repo)


@pytest.mark.asyncio
async def test_list_records_by_filter(use_case):
    records, next_cursor = await use_case.execute(
        limit=10,
        filter={RecordFilter.NCA_TYPE: "REG"},
    )
    assert len(records) <= 10
    if records:
        assert next_cursor == records[-1].id


@pytest.mark.asyncio
async def test_list_records_by_filter_empty_cursor(use_case):
    with pytest.raises(ValidationError, match="Cursor cannot be an empty string."):
        await use_case.execute(limit=10, filter={RecordFilter.NCA_TYPE: "REG"}, cursor="")


@pytest.mark.asyncio
async def test_list_records_by_filter_limit_zero(use_case):
    records, next_cursor = await use_case.execute(limit=0, filter={RecordFilter.NCA_TYPE: "REG"})
    assert len(records) == 0
    assert next_cursor is None


@pytest.mark.asyncio
async def test_list_records_by_filter_with_cursor(use_case):
    records, next_cursor = await use_case.execute(limit=10, filter=FILTER)
    assert len(records) <= 10
    if records:
        assert next_cursor == records[-1].id
    for record in records:
        assert record.department == RECORD_FILTER_VALUE

    records_next, next_cursor_next = await use_case.execute(
        limit=10, filter=FILTER, cursor=next_cursor
    )
    assert len(records_next) <= 10
    if records_next:
        assert next_cursor_next == records_next[-1].id
    for record in records_next:
        assert record.department == RECORD_FILTER_VALUE


@pytest.mark.asyncio
async def test_list_records_by_filter_with_invalid_cursor(use_case):
    records, next_cursor = await use_case.execute(
        limit=10, filter=FILTER, cursor="nonexistent-id"
    )
    assert len(records) == 0
    assert next_cursor is None


@pytest.mark.asyncio
async def test_list_records_by_filter_with_leading_trailing_spaces_cursor(use_case):
    records, next_cursor = await use_case.execute(
        limit=10, filter=FILTER, cursor=f" {RECORD_ID} "
    )
    assert len(records) <= 10
    if records:
        assert next_cursor == records[-1].id
    for record in records:
        assert record.department == RECORD_FILTER_VALUE


@pytest.mark.asyncio
async def test_list_records_by_filter_with_upper_case_cursor(use_case):
    records, next_cursor = await use_case.execute(
        limit=10, filter=FILTER, cursor=RECORD_ID.upper()
    )
    assert len(records) <= 10
    if records:
        assert next_cursor == records[-1].id
    for record in records:
        assert record.department == RECORD_FILTER_VALUE


@pytest.mark.asyncio
async def test_list_records_by_filter_with_negative_limit(use_case):
    records, next_cursor = await use_case.execute(
        limit=-5, filter=FILTER,
    )
    assert len(records) == 0
    assert next_cursor is None


@pytest.mark.asyncio
async def test_list_records_by_filter_with_no_matching_records(use_case):
    records, next_cursor = await use_case.execute(
        limit=10,
        filter={RecordFilter.DEPARTMENT: "Nonexistent Department"},
    )
    assert len(records) == 0
    assert next_cursor is None
