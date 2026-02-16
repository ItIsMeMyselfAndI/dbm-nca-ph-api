import pytest

from src.core.entities.record_filter import RecordFilter


@pytest.fixture
def repo():
    from tests.mock.repositories.mock_record_repository import (
        MockRecordRepository,
    )

    return MockRecordRepository()


def test_list_records_by_filter(repo):
    filter = {RecordFilter.DEPARTMENT: "Department of Health (DOH)"}
    records = repo.list_records_by_filter(limit=10, filter=filter)
    assert len(records) == 6
    for record in records:
        assert record.department == "Department of Health (DOH)"


def test_list_records_by_filter_with_cursor(repo):
    filter = {RecordFilter.DEPARTMENT: "Department of Health (DOH)"}
    first_page = repo.list_records_by_filter(limit=5, filter=filter)
    assert len(first_page) == 5

    second_page = repo.list_records_by_filter(
        limit=5, filter=filter, cursor=first_page[-1].id
    )
    assert len(second_page) == 1


def test_list_records_by_filter_with_invalid_cursor(repo):
    filter = {RecordFilter.DEPARTMENT: "Department of Health (DOH)"}
    with pytest.raises(ValueError) as exc_info:
        repo.list_records_by_filter(limit=5, filter=filter, cursor="nonexistent-id")
    assert str(exc_info.value) == "Cursor with ID nonexistent-id not found."


def test_list_records_by_filter_with_empty_cursor(repo):
    filter = {RecordFilter.DEPARTMENT: "Department of Health (DOH)"}
    records = repo.list_records_by_filter(limit=5, filter=filter, cursor="")
    assert len(records) == 5
    for record in records:
        assert record.department == "Department of Health (DOH)"


def test_list_records_by_filter_with_none_cursor(repo):
    filter = {RecordFilter.DEPARTMENT: "Department of Health (DOH)"}
    records = repo.list_records_by_filter(limit=5, filter=filter, cursor=None)
    assert len(records) == 5
    for record in records:
        assert record.department == "Department of Health (DOH)"


def test_list_records_by_filter_with_leading_trailing_spaces_cursor(repo):
    filter = {RecordFilter.DEPARTMENT: "Department of Health (DOH)"}
    records = repo.list_records_by_filter(
        limit=5, filter=filter, cursor=" 91e80926-ea6a-48d1-bb63-875b4924ecec "
    )
    assert len(records) == 5


def test_list_records_by_filter_with_upper_case_cursor(repo):
    filter = {RecordFilter.DEPARTMENT: "Department of Health (DOH)"}
    records = repo.list_records_by_filter(
        limit=5, filter=filter, cursor="91E80926-EA6A-48D1-BB63-875B4924ECEC"
    )
    assert len(records) == 5


def test_list_records_by_filter_with_limit_zero(repo):
    filter = {RecordFilter.DEPARTMENT: "Department of Health (DOH)"}
    records = repo.list_records_by_filter(limit=0, filter=filter)
    assert len(records) == 0


def test_list_records_by_filter_with_limit_exceeding_total(repo):
    filter = {RecordFilter.DEPARTMENT: "Department of Health (DOH)"}
    records = repo.list_records_by_filter(limit=100, filter=filter)
    assert len(records) == 6


# def test_list_records_by_filter_with_negative_limit(repo):
#     filter = {RecordFilter.DEPARTMENT: "Department of Health (DOH)"}
#     records = repo.list_records_by_filter(limit=-5, filter=filter)
#     assert len(records) == 0


def test_list_records_by_filter_with_no_matching_records(repo):
    filter = {RecordFilter.DEPARTMENT: "Nonexistent Department"}
    records = repo.list_records_by_filter(limit=10, filter=filter)
    assert len(records) == 0
