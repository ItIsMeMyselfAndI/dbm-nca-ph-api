import pytest

from src.core.use_cases.record.get_record_by_id import GetRecordByID

RECORD_ID = "40e718ad-5704-44cd-a3f1-a64f2c191538"


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


def test_get_record_by_id(use_case: GetRecordByID):
    record = use_case.execute(RECORD_ID)
    assert record.id == RECORD_ID


def test_get_record_by_id_not_found(use_case: GetRecordByID):
    with pytest.raises(ValueError) as exc_info:
        use_case.execute("nonexistent-id")
    assert str(exc_info.value) == "Record with ID nonexistent-id not found."


def test_get_record_by_id_empty_string(use_case: GetRecordByID):
    with pytest.raises(ValueError) as exc_info:
        use_case.execute("")
    assert str(exc_info.value) == "Record with ID  not found."


def test_get_record_by_id_in_upper_case(use_case: GetRecordByID):
    record = use_case.execute(RECORD_ID.upper())
    assert record.id == RECORD_ID


def test_get_record_by_id_leading_trailing_spaces(use_case: GetRecordByID):
    record = use_case.execute(f" {RECORD_ID} ")
    assert record.id == RECORD_ID
