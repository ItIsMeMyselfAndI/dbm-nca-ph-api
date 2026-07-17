import pytest

from src.core.entities.record_filter import RecordFilter


@pytest.fixture
def repo():
    from tests.mock.repositories.mock_record_repository import (
        MockRecordRepository,
    )

    return MockRecordRepository()


FILTER = {RecordFilter.DEPARTMENT: "Department of Health (DOH)"}


def test_list_records_by_filter(repo):
    records = repo.list_records_by_filter(limit=10, filter=FILTER)
    assert len(records) == 10
    for record in records:
        assert record.department == "Department of Health (DOH)"


def test_list_records_by_filter_with_cursor(repo):
    first_page = repo.list_records_by_filter(limit=5, filter=FILTER)
    assert len(first_page) == 5

    second_page = repo.list_records_by_filter(
        limit=5, filter=FILTER, cursor=first_page[-1].id
    )
    assert len(second_page) == 5


def test_list_records_by_filter_by_nca_type(repo):
    filter = {RecordFilter.NCA_TYPE: "TLRG"}
    records = repo.list_records_by_filter(limit=20, filter=filter)
    assert len(records) == 13
    for record in records:
        assert record.nca_type == "TLRG"


def test_list_records_by_filter_by_nca_type_with_cursor(repo):
    filter = {RecordFilter.NCA_TYPE: "TLRG"}
    first_page = repo.list_records_by_filter(limit=5, filter=filter)
    assert len(first_page) == 5

    second_page = repo.list_records_by_filter(
        limit=5, filter=filter, cursor=first_page[-1].id
    )
    assert len(second_page) == 5

    third_page = repo.list_records_by_filter(
        limit=5, filter=filter, cursor=second_page[-1].id
    )
    assert len(third_page) == 3


def test_list_records_by_filter_by_release_id(repo):
    filter = {RecordFilter.RELEASE_ID: "id_2024"}
    records = repo.list_records_by_filter(limit=5, filter=filter)
    assert len(records) == 5
    for record in records:
        assert record.release_id == "id_2024"


def test_list_records_by_filter_with_invalid_cursor(repo):
    with pytest.raises(ValueError) as exc_info:
        repo.list_records_by_filter(limit=5, filter=FILTER, cursor="nonexistent-id")
    assert str(exc_info.value) == "Cursor with ID nonexistent-id not found."


def test_list_records_by_filter_with_empty_cursor(repo):
    records = repo.list_records_by_filter(limit=5, filter=FILTER, cursor="")
    assert len(records) == 5
    for record in records:
        assert record.department == "Department of Health (DOH)"


def test_list_records_by_filter_with_none_cursor(repo):
    records = repo.list_records_by_filter(limit=5, filter=FILTER, cursor=None)
    assert len(records) == 5
    for record in records:
        assert record.department == "Department of Health (DOH)"


def test_list_records_by_filter_with_leading_trailing_spaces_cursor(repo):
    records = repo.list_records_by_filter(
        limit=5, filter=FILTER, cursor=" f7f65824-481a-4d98-befc-d7287f614060 "
    )
    assert len(records) == 5


def test_list_records_by_filter_with_upper_case_cursor(repo):
    records = repo.list_records_by_filter(
        limit=5, filter=FILTER, cursor="F7F65824-481A-4D98-BEFC-D7287F614060"
    )
    assert len(records) == 5


def test_list_records_by_filter_with_limit_zero(repo):
    records = repo.list_records_by_filter(limit=0, filter=FILTER)
    assert len(records) == 0


def test_list_records_by_filter_with_limit_exceeding_total(repo):
    records = repo.list_records_by_filter(limit=100, filter=FILTER)
    assert len(records) == 86


def test_list_records_by_filter_with_no_matching_records(repo):
    filter = {RecordFilter.DEPARTMENT: "Nonexistent Department"}
    records = repo.list_records_by_filter(limit=10, filter=filter)
    assert len(records) == 0
