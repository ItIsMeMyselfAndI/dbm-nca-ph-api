import pytest

from src.core.exceptions import NotFoundError


@pytest.fixture
def repo():
    from tests.mock.repositories_async.mock_async_record_repository import (
        MockAsyncRecordRepository,
    )
    return MockAsyncRecordRepository()


@pytest.fixture
def use_case(repo):
    from src.core.use_cases.v2.record.get_record_by_id import GetRecordByID
    return GetRecordByID(repo)


@pytest.mark.asyncio
async def test_get_record_by_id(use_case):
    record = await use_case.execute("a729caee-c88f-416b-ba35-fca60a553aaa")
    assert record.id == "a729caee-c88f-416b-ba35-fca60a553aaa"


@pytest.mark.asyncio
async def test_get_record_by_id_not_found(use_case):
    with pytest.raises(NotFoundError):
        await use_case.execute("nonexistent-id")


@pytest.mark.asyncio
async def test_get_record_by_id_empty_string(use_case):
    with pytest.raises(NotFoundError):
        await use_case.execute("")


@pytest.mark.asyncio
async def test_get_record_by_id_upper_case(use_case):
    record = await use_case.execute("A729CAEE-C88F-416B-BA35-FCA60A553AAA")
    assert record.id == "a729caee-c88f-416b-ba35-fca60a553aaa"


@pytest.mark.asyncio
async def test_get_record_by_id_leading_trailing_spaces(use_case):
    record = await use_case.execute(" a729caee-c88f-416b-ba35-fca60a553aaa ")
    assert record.id == "a729caee-c88f-416b-ba35-fca60a553aaa"
