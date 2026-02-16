import pytest


@pytest.fixture
def repo():
    from tests.mock.repositories.mock_record_repository import (
        MockRecordRepository,
    )

    return MockRecordRepository()


@pytest.fixture
def use_case(repo):
    from src.core.use_cases.record.get_record_by_id import GetRecordByID

    return GetRecordByID(repo)


def test_get_record_by_id(use_case):
    record = use_case.execute("91e80926-ea6a-48d1-bb63-875b4924ecec")
    assert record.id == "91e80926-ea6a-48d1-bb63-875b4924ecec"


def test_get_record_by_id_not_found(use_case):
    with pytest.raises(ValueError) as exc_info:
        use_case.execute("nonexistent-id")
    assert str(exc_info.value) == "Record with ID nonexistent-id not found."


def test_get_record_by_id_empty_string(use_case):
    with pytest.raises(ValueError) as exc_info:
        use_case.execute("")
    assert str(exc_info.value) == "Record with ID  not found."


def test_get_record_by_id_in_upper_case(use_case):
    record = use_case.execute("91E80926-EA6A-48D1-BB63-875B4924ECEC")
    assert record.id == "91e80926-ea6a-48d1-bb63-875b4924ecec"


def test_get_record_by_id_leading_trailing_spaces(use_case):
    record = use_case.execute(" 91e80926-ea6a-48d1-bb63-875b4924ecec ")
    assert record.id == "91e80926-ea6a-48d1-bb63-875b4924ecec"
