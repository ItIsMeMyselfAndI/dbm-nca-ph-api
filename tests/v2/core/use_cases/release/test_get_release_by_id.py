import pytest

from src.core.exceptions import NotFoundError


@pytest.fixture
def repo():
    from tests.mock.repositories_async.mock_async_release_repository import (
        MockAsyncReleaseRepository,
    )
    return MockAsyncReleaseRepository()


@pytest.fixture
def use_case(repo):
    from src.core.use_cases.v2.release.get_release_by_id import GetReleaseById
    return GetReleaseById(repo)


@pytest.mark.asyncio
async def test_get_release_by_id(use_case):
    release = await use_case.execute("id_2024")
    assert release.id == "id_2024"


@pytest.mark.asyncio
async def test_get_release_by_id_not_found(use_case):
    with pytest.raises(NotFoundError):
        await use_case.execute("nonexistent-id")


@pytest.mark.asyncio
async def test_get_release_by_id_empty_string(use_case):
    with pytest.raises(NotFoundError):
        await use_case.execute("")


@pytest.mark.asyncio
async def test_get_release_by_id_upper_case(use_case):
    release = await use_case.execute("ID_2024")
    assert release.id == "id_2024"


@pytest.mark.asyncio
async def test_get_release_by_id_leading_trailing_spaces(use_case):
    release = await use_case.execute(" id_2024 ")
    assert release.id == "id_2024"
