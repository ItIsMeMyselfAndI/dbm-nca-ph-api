import pytest


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


def test_list_records(use_case):
    records, next_cursor = use_case.execute(limit=10)
    assert len(records) == 10
    assert next_cursor is not None


def test_list_records_with_cursor(use_case):
    records, next_cursor = use_case.execute(limit=5)
    assert len(records) == 5
    assert next_cursor is not None

    records_next, next_cursor_next = use_case.execute(limit=5, cursor=next_cursor)
    assert len(records_next) == 5
    assert next_cursor_next is not None


def test_list_records_with_invalid_cursor(use_case):
    with pytest.raises(ValueError) as exc_info:
        use_case.execute(limit=5, cursor="nonexistent-id")
    assert str(exc_info.value) == "Cursor with ID nonexistent-id not found."


def test_list_records_with_empty_cursor(use_case):
    with pytest.raises(ValueError) as exc_info:
        use_case.execute(limit=5, cursor="")
    assert str(exc_info.value) == "Cursor cannot be an empty string."


def test_list_records_with_leading_trailing_spaces_cursor(use_case):
    records, next_cursor = use_case.execute(
        limit=5, cursor=" 91e80926-ea6a-48d1-bb63-875b4924ecec "
    )
    assert len(records) == 5
    assert next_cursor is not None


def test_list_records_with_upper_case_cursor(use_case):
    records, next_cursor = use_case.execute(
        limit=5, cursor="91E80926-EA6A-48D1-BB63-875B4924ECEC"
    )
    assert len(records) == 5
    assert next_cursor is not None


def test_list_records_with_limit_zero(use_case):
    records, next_cursor = use_case.execute(limit=0)
    assert len(records) == 0
    assert next_cursor is None


def test_list_records_with_limit_exceeding_total(use_case):
    records, next_cursor = use_case.execute(limit=100)
    assert len(records) == 40
    assert next_cursor is None


def test_list_records_with_negative_limit(use_case):
    records, next_cursor = use_case.execute(limit=-5)
    assert len(records) == 0
    assert next_cursor is None
