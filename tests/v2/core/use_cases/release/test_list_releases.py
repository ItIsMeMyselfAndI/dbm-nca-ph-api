import pytest

from src.core.exceptions import ValidationError

RELEASE_ID = "id_2024"


@pytest.fixture
def repo():
    from tests.mock.repositories_async.mock_async_release_repository import (
        MockAsyncReleaseRepository,
    )
    return MockAsyncReleaseRepository()


@pytest.fixture
def use_case(repo):
    from src.core.use_cases.v2.release.list_releases import ListReleases
    return ListReleases(repo)


@pytest.mark.asyncio
async def test_list_releases(use_case):
    releases, next_cursor = await use_case.execute(limit=2)
    assert len(releases) <= 2
    if releases:
        assert next_cursor == releases[-1].id


@pytest.mark.asyncio
async def test_list_releases_with_cursor(use_case):
    releases, next_cursor = await use_case.execute(limit=2)
    assert len(releases) <= 2
    next_cursor_val = next_cursor

    releases_next, next_cursor_next = await use_case.execute(limit=2, cursor=next_cursor_val)
    assert len(releases_next) <= 2
    if releases_next:
        assert next_cursor_next == releases_next[-1].id


@pytest.mark.asyncio
async def test_list_releases_with_empty_cursor(use_case):
    with pytest.raises(ValidationError, match="Cursor cannot be an empty string."):
        await use_case.execute(limit=2, cursor="")


@pytest.mark.asyncio
async def test_list_releases_with_leading_trailing_spaces_cursor(use_case):
    releases, next_cursor = await use_case.execute(limit=2, cursor=f" {RELEASE_ID} ")
    assert len(releases) <= 2
    if releases:
        assert next_cursor == releases[-1].id


@pytest.mark.asyncio
async def test_list_releases_with_upper_case_cursor(use_case):
    releases, next_cursor = await use_case.execute(limit=2, cursor=RELEASE_ID.upper())
    assert len(releases) <= 2
    if releases:
        assert next_cursor == releases[-1].id


@pytest.mark.asyncio
async def test_list_releases_with_limit_zero(use_case):
    releases, next_cursor = await use_case.execute(limit=0)
    assert len(releases) == 0
    assert next_cursor is None


@pytest.mark.asyncio
async def test_list_releases_with_negative_limit(use_case):
    releases, next_cursor = await use_case.execute(limit=-5)
    assert len(releases) == 0
    assert next_cursor is None
