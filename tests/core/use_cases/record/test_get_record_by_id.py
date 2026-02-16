import pytest


@pytest.fixture
def repo():
    from tests.infrastructure.db.mock_record_repository import (
        MockRecordRepository,
    )

    return MockRecordRepository()


def test_get_record_by_id(repo):
    record = repo.get_record_by_id("91e80926-ea6a-48d1-bb63-875b4924ecec")
    assert record.id == "91e80926-ea6a-48d1-bb63-875b4924ecec"
    assert record.nca_number == "NCA-ROIX-24-0000001"
    assert record.nca_type == "REG"
    assert record.released_date == "2024-01-02T07:10:16+00:00"
    assert record.department == "Department of Health (DOH)"
    assert (
        record.purpose
        == "To cover the regular operating and RLIP requirements for the first quarter (January to March 2024)"
    )
    assert record.release_id == "id_2024"


def test_get_record_by_id_not_found(repo):
    with pytest.raises(ValueError) as exc_info:
        repo.get_record_by_id("nonexistent-id")
    assert str(exc_info.value) == "Record with ID nonexistent-id not found."


def test_get_record_by_id_empty_string(repo):
    with pytest.raises(ValueError) as exc_info:
        repo.get_record_by_id("")
    assert str(exc_info.value) == "Record with ID  not found."


def test_get_record_by_id_none(repo):
    with pytest.raises(ValueError) as exc_info:
        repo.get_record_by_id(None)
    assert str(exc_info.value) == "Record with ID None not found."


def test_get_record_by_id_case_sensitivity(repo):
    with pytest.raises(ValueError) as exc_info:
        repo.get_record_by_id("91E80926-EA6A-48D1-BB63-875B4924ECEC")
    assert (
        str(exc_info.value)
        == "Record with ID 91E80926-EA6A-48D1-BB63-875B4924ECEC not found."
    )


def test_get_record_by_id_leading_trailing_spaces(repo):
    with pytest.raises(ValueError) as exc_info:
        repo.get_record_by_id(" 91e80926-ea6a-48d1-bb63-875b4924ecec ")
    assert (
        str(exc_info.value)
        == "Record with ID  91e80926-ea6a-48d1-bb63-875b4924ecec  not found."
    )


def test_get_record_by_id_with_leading_trailing_spaces(repo):
    with pytest.raises(ValueError) as exc_info:
        repo.get_record_by_id(" 91e80926-ea6a-48d1-bb63-875b4924ecec ")
    assert (
        str(exc_info.value)
        == "Record with ID  91e80926-ea6a-48d1-bb63-875b4924ecec  not found."
    )


def test_get_record_by_id_with_case_sensitivity(repo):
    with pytest.raises(ValueError) as exc_info:
        repo.get_record_by_id("91E80926-EA6A-48D1-BB63-875B4924ECEC")
    assert (
        str(exc_info.value)
        == "Record with ID 91E80926-EA6A-48D1-BB63-875B4924ECEC not found."
    )
