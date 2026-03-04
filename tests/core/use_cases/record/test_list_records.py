import pytest

from src.core.use_cases.record.list_records import ListRecords

RECORD_ID = "40e718ad-5704-44cd-a3f1-a64f2c191538"
LIMIT_ROW_COUNT = 10


@pytest.fixture
def repo():
    from tests.mock.repositories.mock_record_repository import (
        MockRecordRepository,
    )

    return MockRecordRepository()


@pytest.fixture
def use_case(repo):
    from src.core.use_cases.record.list_records import ListRecords

    return ListRecords(repo)


def test_list_records(use_case: ListRecords):
    records, next_cursor = use_case.execute(limit=LIMIT_ROW_COUNT)
    assert len(records) <= LIMIT_ROW_COUNT
    if len(records) != 0:
        assert next_cursor == records[-1].id


def test_list_records_with_cursor(use_case: ListRecords):
    records, next_cursor = use_case.execute(limit=LIMIT_ROW_COUNT)
    assert len(records) <= LIMIT_ROW_COUNT
    if len(records) != 0:
        assert next_cursor == records[-1].id

    records_next, next_cursor_next = use_case.execute(
        limit=LIMIT_ROW_COUNT, cursor=next_cursor
    )
    assert len(records_next) <= LIMIT_ROW_COUNT
    if len(records_next) != 0:
        assert next_cursor_next == records_next[-1].id


def test_list_records_with_invalid_cursor(use_case: ListRecords):
    with pytest.raises(ValueError) as exc_info:
        use_case.execute(limit=LIMIT_ROW_COUNT, cursor="nonexistent-id")
    assert str(exc_info.value) == "Cursor with ID nonexistent-id not found."


def test_list_records_with_empty_cursor(use_case: ListRecords):
    with pytest.raises(ValueError) as exc_info:
        use_case.execute(limit=LIMIT_ROW_COUNT, cursor="")
    assert str(exc_info.value) == "Cursor cannot be an empty string."


def test_list_records_with_leading_trailing_spaces_cursor(use_case: ListRecords):
    records, next_cursor = use_case.execute(
        limit=LIMIT_ROW_COUNT, cursor=f" {RECORD_ID} "
    )
    assert len(records) <= LIMIT_ROW_COUNT
    if len(records) != 0:
        assert next_cursor == records[-1].id


def test_list_records_with_upper_case_cursor(use_case: ListRecords):
    records, next_cursor = use_case.execute(
        limit=LIMIT_ROW_COUNT, cursor=RECORD_ID.upper()
    )
    assert len(records) <= LIMIT_ROW_COUNT
    if len(records) != 0:
        assert next_cursor == records[-1].id


def test_list_records_with_limit_zero(use_case: ListRecords):
    records, next_cursor = use_case.execute(limit=0)
    assert len(records) == 0
    assert next_cursor is None


def test_list_records_with_negative_limit(use_case: ListRecords):
    records, next_cursor = use_case.execute(limit=-5)
    assert len(records) == 0
    assert next_cursor is None
