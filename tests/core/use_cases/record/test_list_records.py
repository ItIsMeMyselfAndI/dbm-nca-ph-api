import pytest


@pytest.fixture
def repo():
    from tests.infrastructure.db.mock_record_repository import (
        MockRecordRepository,
    )

    return MockRecordRepository()


def test_list_records(repo):
    records = repo.list_records(limit=10)
    assert len(records) == 10
    assert records[0].id == "91e80926-ea6a-48d1-bb63-875b4924ecec"
    assert records[0].nca_number == "NCA-ROIX-24-0000001"
    assert records[0].nca_type == "REG"
    assert records[0].released_date == "2024-01-02T07:10:16+00:00"
    assert records[0].department == "Department of Health (DOH)"
    assert (
        records[0].purpose
        == "To cover the regular operating and RLIP requirements for the first quarter (January to March 2024)"
    )
    assert records[0].release_id == "id_2024"


def test_list_records_with_cursor(repo):
    first_page = repo.list_records(limit=5)
    assert len(first_page) == 5
    assert first_page[0].id == "91e80926-ea6a-48d1-bb63-875b4924ecec"

    second_page = repo.list_records(limit=5, cursor=first_page[-1].id)
    assert len(second_page) == 5
    assert second_page[0].id == "f21bf45a-8791-4eb1-ae56-5c4f41875b3d"


def test_list_records_with_invalid_cursor(repo):
    with pytest.raises(ValueError) as exc_info:
        repo.list_records(limit=5, cursor="nonexistent-id")
    assert str(exc_info.value) == "Cursor with ID nonexistent-id not found."


def test_list_records_with_empty_cursor(repo):
    with pytest.raises(ValueError) as exc_info:
        repo.list_records(limit=5, cursor="")
    assert str(exc_info.value) == "Cursor with ID  not found."


def test_list_records_with_none_cursor(repo):
    with pytest.raises(ValueError) as exc_info:
        repo.list_records(limit=5, cursor=None)
    assert str(exc_info.value) == "Cursor with ID None not found."


def test_list_records_with_leading_trailing_spaces_cursor(repo):
    with pytest.raises(ValueError) as exc_info:
        repo.list_records(limit=5, cursor=" 91e80926-ea6a-48d1-bb63-875b4924ecec ")
    assert (
        str(exc_info.value)
        == "Cursor with ID  91e80926-ea6a-48d1-bb63-875b4924ecec  not found."
    )


def test_list_records_with_case_sensitivity_cursor(repo):
    with pytest.raises(ValueError) as exc_info:
        repo.list_records(limit=5, cursor="91E80926-EA6A-48D1-BB63-875B4924ECEC")
    assert (
        str(exc_info.value)
        == "Cursor with ID 91E80926-EA6A-48D1-BB63-875B4924ECEC not found."
    )


def test_list_records_with_limit_zero(repo):
    records = repo.list_records(limit=0)
    assert len(records) == 0


def test_list_records_with_limit_exceeding_total(repo):
    records = repo.list_records(limit=100)
    assert len(records) == 40


def test_list_records_with_negative_limit(repo):
    with pytest.raises(ValueError) as exc_info:
        repo.list_records(limit=-5)
    assert str(exc_info.value) == "Limit must be a non-negative integer."
