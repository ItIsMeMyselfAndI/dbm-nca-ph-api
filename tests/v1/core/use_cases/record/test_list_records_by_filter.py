import pytest

from src.core.entities.record_filter import RecordFilter

RECORD_ID = "40e718ad-5704-44cd-a3f1-a64f2c191538"
RECORD_FILTER_KEY = RecordFilter.DEPARTMENT
RECORD_FILTER_VALUE = "Department of Education (DepEd)"
FILTER = {RECORD_FILTER_KEY: RECORD_FILTER_VALUE}
LIMIT_ROW_COUNT = 10


@pytest.fixture
def repo():
    from tests.mock.repositories.mock_record_repository import (
        MockRecordRepository,
    )

    return MockRecordRepository()


@pytest.fixture
def use_case(repo):
    from src.core.use_cases.v1.record.list_records_by_filter import ListRecordsByFilter

    return ListRecordsByFilter(repo)


def test_list_records_by_filter(use_case):
    records, next_cursor = use_case.execute(filter=FILTER, limit=LIMIT_ROW_COUNT)
    assert len(records) <= LIMIT_ROW_COUNT
    if len(records) != 0:
        assert next_cursor == records[-1].id
    for record in records:
        assert record.department == RECORD_FILTER_VALUE


def test_list_records_by_filter_with_cursor(use_case):
    records, next_cursor = use_case.execute(filter=FILTER, limit=LIMIT_ROW_COUNT)
    assert len(records) <= LIMIT_ROW_COUNT
    if len(records) != 0:
        assert next_cursor == records[-1].id
    for record in records:
        assert record.department == RECORD_FILTER_VALUE

    records_next, next_cursor_next = use_case.execute(
        filter=FILTER, limit=LIMIT_ROW_COUNT, cursor=next_cursor
    )
    assert len(records_next) <= LIMIT_ROW_COUNT
    if len(records) != 0:
        assert next_cursor_next == records_next[-1].id
    for record in records_next:
        assert record.department == RECORD_FILTER_VALUE


def test_list_records_by_filter_with_invalid_cursor(use_case):
    with pytest.raises(ValueError) as exc_info:
        use_case.execute(filter=FILTER, limit=LIMIT_ROW_COUNT, cursor="nonexistent-id")
    assert str(exc_info.value) == "Cursor with ID nonexistent-id not found."


def test_list_records_by_filter_with_empty_cursor(use_case):
    with pytest.raises(ValueError) as exc_info:
        use_case.execute(filter=FILTER, limit=LIMIT_ROW_COUNT, cursor="")
    assert str(exc_info.value) == "Cursor cannot be an empty string."


def test_list_records_by_filter_with_leading_trailing_spaces_cursor(use_case):
    records, next_cursor = use_case.execute(
        filter=FILTER,
        limit=LIMIT_ROW_COUNT,
        cursor=f" {RECORD_ID} ",
    )
    assert len(records) <= LIMIT_ROW_COUNT
    if len(records) != 0:
        assert next_cursor == records[-1].id


def test_list_records_by_filter_with_upper_case_cursor(use_case):
    records, next_cursor = use_case.execute(
        filter=FILTER,
        limit=LIMIT_ROW_COUNT,
        cursor=RECORD_ID.upper(),
    )
    assert len(records) <= LIMIT_ROW_COUNT
    if len(records) != 0:
        assert next_cursor == records[-1].id


def test_list_records_by_filter_with_limit_zero(use_case):
    records, next_cursor = use_case.execute(filter=FILTER, limit=0)
    assert len(records) == 0
    assert next_cursor is None


def test_list_records_by_filter_with_negative_limit(use_case):
    records, next_cursor = use_case.execute(filter=FILTER, limit=-5)
    assert len(records) == 0
    assert next_cursor is None


def test_list_records_by_filter_with_no_matching_records(use_case):
    records, next_cursor = use_case.execute(
        filter={RecordFilter.DEPARTMENT: "Nonexistent Department"},
        limit=LIMIT_ROW_COUNT,
    )
    assert len(records) == 0
    assert next_cursor is None
