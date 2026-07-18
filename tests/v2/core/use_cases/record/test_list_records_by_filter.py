import pytest

from src.core.entities.record_filter import RecordFilter
from src.core.exceptions import ValidationError


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
