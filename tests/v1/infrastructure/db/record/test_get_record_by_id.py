import pytest


@pytest.fixture
def repo():
    from tests.mock.repositories.mock_record_repository import (
        MockRecordRepository,
    )

    return MockRecordRepository()


def test_get_record_by_id(repo):
    record = repo.get_record_by_id("91e80926-ea6a-48d1-bb63-875b4924ecec")
    assert record.id == "91e80926-ea6a-48d1-bb63-875b4924ecec"


def test_get_record_by_id_not_found(repo):
    with pytest.raises(ValueError) as exc_info:
        repo.get_record_by_id("nonexistent-id")
    assert str(exc_info.value) == "Record with ID nonexistent-id not found."


def test_get_record_by_id_empty_string(repo):
    with pytest.raises(ValueError) as exc_info:
        repo.get_record_by_id("")
    assert str(exc_info.value) == "Record with ID  not found."


# def test_get_record_by_id_none(repo):
#     with pytest.raises(ValueError) as exc_info:
#         repo.get_record_by_id(None)
#     assert str(exc_info.value) == "Record with ID None not found."


def test_get_record_by_id_in_upper_case(repo):
    record = repo.get_record_by_id("91E80926-EA6A-48D1-BB63-875B4924ECEC")
    assert record.id == "91e80926-ea6a-48d1-bb63-875b4924ecec"


def test_get_record_by_id_leading_trailing_spaces(repo):
    record = repo.get_record_by_id(" 91e80926-ea6a-48d1-bb63-875b4924ecec ")
    assert record.id == "91e80926-ea6a-48d1-bb63-875b4924ecec"
