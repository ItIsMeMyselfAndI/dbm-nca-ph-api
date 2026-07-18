import pytest


@pytest.fixture
def repo():
    from tests.mock.repositories.mock_record_repository import (
        MockRecordRepository,
    )

    return MockRecordRepository()


def test_list_records(repo):
    records = repo.list_records(limit=10)
    assert len(records) == 10
    assert records[0].id == "91e80926-ea6a-48d1-bb63-875b4924ecec"


def test_list_records_with_cursor(repo):
    first_page = repo.list_records(limit=5)
    assert len(first_page) == 5

    second_page = repo.list_records(limit=5, cursor=first_page[-1].id)
    assert len(second_page) == 5


def test_list_records_with_invalid_cursor(repo):
    with pytest.raises(ValueError) as exc_info:
        repo.list_records(limit=5, cursor="nonexistent-id")
    assert str(exc_info.value) == "Cursor with ID nonexistent-id not found."


def test_list_records_with_empty_cursor(repo):
    records = repo.list_records(limit=5, cursor="")
    assert len(records) == 5


def test_list_records_with_none_cursor(repo):
    records = repo.list_records(limit=5, cursor=None)
    assert len(records) == 5


def test_list_records_with_leading_trailing_spaces_cursor(repo):
    records = repo.list_records(
        limit=5, cursor=" 91e80926-ea6a-48d1-bb63-875b4924ecec "
    )
    assert len(records) == 5


def test_list_records_with_upper_case_cursor(repo):
    records = repo.list_records(limit=5, cursor="91E80926-EA6A-48D1-BB63-875B4924ECEC")
    assert len(records) == 5


def test_list_records_with_limit_zero(repo):
    records = repo.list_records(limit=0)
    assert len(records) == 0


def test_list_records_with_limit_exceeding_total(repo):
    records = repo.list_records(limit=100)
    assert len(records) == 40


#
#
# def test_list_records_with_negative_limit(repo):
#     records = repo.list_records(limit=-5)
#     assert len(records) == 0
