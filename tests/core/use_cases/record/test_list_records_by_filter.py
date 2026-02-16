import pytest

from src.core.entities.record_filter import RecordFilter


@pytest.fixture
def repo():
    from tests.mock.repositories.mock_record_repository import (
        MockRecordRepository,
    )

    return MockRecordRepository()


@pytest.fixture
def use_case(repo):
    from src.core.use_cases.record.list_records_by_filter import ListRecordsByFilter

    return ListRecordsByFilter(repo)


def test_list_records_by_filter(use_case):
    filter = {RecordFilter.DEPARTMENT: "Department of Health (DOH)"}
    records, next_cursor = use_case.execute(filter=filter, limit=10)
    assert len(records) == 6
    assert next_cursor is None
    for record in records:
        assert record.department == "Department of Health (DOH)"


def test_list_records_by_filter_with_cursor(use_case):
    filter = {RecordFilter.DEPARTMENT: "Department of Health (DOH)"}
    records, next_cursor = use_case.execute(filter=filter, limit=5)
    assert len(records) == 5
    assert next_cursor is not None
    for record in records:
        assert record.department == "Department of Health (DOH)"

    records_next, next_cursor_next = use_case.execute(
        filter=filter, limit=5, cursor=next_cursor
    )
    assert len(records_next) == 1
    assert next_cursor_next is None
    for record in records_next:
        assert record.department == "Department of Health (DOH)"


def test_list_records_by_filter_with_invalid_cursor(use_case):
    filter = {RecordFilter.DEPARTMENT: "Department of Health (DOH)"}
    with pytest.raises(ValueError) as exc_info:
        use_case.execute(filter=filter, limit=5, cursor="nonexistent-id")
    assert str(exc_info.value) == "Cursor with ID nonexistent-id not found."


def test_list_records_by_filter_with_empty_cursor(use_case):
    filter = {RecordFilter.DEPARTMENT: "Department of Health (DOH)"}
    with pytest.raises(ValueError) as exc_info:
        use_case.execute(filter=filter, limit=5, cursor="")
    assert str(exc_info.value) == "Cursor with ID  not found."


def test_list_records_by_filter_with_leading_trailing_spaces_cursor(use_case):
    filter = {RecordFilter.DEPARTMENT: "Department of Health (DOH)"}
    with pytest.raises(ValueError) as exc_info:
        use_case.execute(
            filter=filter,
            limit=5,
            cursor=" 91e80926-ea6a-48d1-bb63-875b4924ecec ",
        )
    assert (
        str(exc_info.value)
        == "Cursor with ID  91e80926-ea6a-48d1-bb63-875b4924ecec  not found."
    )


def test_list_records_by_filter_with_case_sensitivity_cursor(use_case):
    filter = {RecordFilter.DEPARTMENT: "Department of Health (DOH)"}
    with pytest.raises(ValueError) as exc_info:
        use_case.execute(
            filter=filter,
            limit=5,
            cursor="91E80926-EA6A-48D1-BB63-875B4924ECEC",
        )
    assert (
        str(exc_info.value)
        == "Cursor with ID 91E80926-EA6A-48D1-BB63-875B4924ECEC not found."
    )


def test_list_records_by_filter_with_limit_zero(use_case):
    filter = {RecordFilter.DEPARTMENT: "Department of Health (DOH)"}
    records, next_cursor = use_case.execute(filter=filter, limit=0)
    assert len(records) == 0
    assert next_cursor is None


def test_list_records_by_filter_with_limit_exceeding_total(use_case):
    filter = {RecordFilter.DEPARTMENT: "Department of Health (DOH)"}
    records, next_cursor = use_case.execute(filter=filter, limit=100)
    assert len(records) == 6
    assert next_cursor is None


def test_list_records_by_filter_with_negative_limit(use_case):
    filter = {RecordFilter.DEPARTMENT: "Department of Health (DOH)"}
    records, next_cursor = use_case.execute(filter=filter, limit=-5)
    assert len(records) == 0
    assert next_cursor is None


def test_list_records_by_filter_with_no_matching_records(use_case):
    filter = {RecordFilter.DEPARTMENT: "Nonexistent Department"}
    records, next_cursor = use_case.execute(filter=filter, limit=10)
    assert len(records) == 0
    assert next_cursor is None
