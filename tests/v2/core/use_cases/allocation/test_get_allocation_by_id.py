import pytest

from src.core.exceptions import NotFoundError


@pytest.fixture
def repo():
    from tests.mock.repositories_async.mock_async_allocation_repository import (
        MockAsyncAllocationRepository,
    )
    return MockAsyncAllocationRepository()


@pytest.fixture
def use_case(repo):
    from src.core.use_cases.v2.allocation.get_allocation_by_id import GetAllocationByID
    return GetAllocationByID(repo)


@pytest.mark.asyncio
async def test_get_allocation_by_id(use_case):
    allocation = await use_case.execute("0000a66b-0265-4b42-adfe-559f98646c91")
    assert allocation.id == "0000a66b-0265-4b42-adfe-559f98646c91"


@pytest.mark.asyncio
async def test_get_allocation_by_id_not_found(use_case):
    with pytest.raises(NotFoundError):
        await use_case.execute("nonexistent-id")


@pytest.mark.asyncio
async def test_get_allocation_by_id_empty_string(use_case):
    with pytest.raises(NotFoundError):
        await use_case.execute("")


@pytest.mark.asyncio
async def test_get_allocation_by_id_upper_case(use_case):
    allocation = await use_case.execute("0000A66B-0265-4B42-ADFE-559F98646C91")
    assert allocation.id == "0000a66b-0265-4b42-adfe-559f98646c91"


@pytest.mark.asyncio
async def test_get_allocation_by_id_leading_trailing_spaces(use_case):
    allocation = await use_case.execute(" 0000a66b-0265-4b42-adfe-559f98646c91 ")
    assert allocation.id == "0000a66b-0265-4b42-adfe-559f98646c91"
