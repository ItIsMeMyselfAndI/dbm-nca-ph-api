import pytest

from src.core.exceptions import ValidationError


@pytest.fixture
def repo():
    from tests.mock.repositories_async.mock_async_record_repository import (
        MockAsyncRecordRepository,
    )
    return MockAsyncRecordRepository()


@pytest.fixture
def use_case(repo):
    from src.core.use_cases.v2.record.list_records import ListRecords
    return ListRecords(repo)


@pytest.mark.asyncio
async def test_list_records(use_case):
    records, next_cursor = await use_case.execute(limit=10)
    assert len(records) <= 10
    if records:
        assert next_cursor == records[-1].id


@pytest.mark.asyncio
async def test_list_records_with_cursor(use_case):
    records, next_cursor = await use_case.execute(limit=5)
    next_cursor_val = next_cursor
    records_next, next_cursor_next = await use_case.execute(limit=5, cursor=next_cursor_val)
    assert len(records_next) <= 5
    if records_next:
        assert next_cursor_next == records_next[-1].id


@pytest.mark.asyncio
async def test_list_records_with_empty_cursor(use_case):
    with pytest.raises(ValidationError, match="Cursor cannot be an empty string."):
        await use_case.execute(limit=5, cursor="")


@pytest.mark.asyncio
async def test_list_records_with_limit_zero(use_case):
    records, next_cursor = await use_case.execute(limit=0)
    assert len(records) == 0
    assert next_cursor is None


@pytest.mark.asyncio
async def test_list_records_with_negative_limit(use_case):
    records, next_cursor = await use_case.execute(limit=-5)
    assert len(records) == 0
    assert next_cursor is None
