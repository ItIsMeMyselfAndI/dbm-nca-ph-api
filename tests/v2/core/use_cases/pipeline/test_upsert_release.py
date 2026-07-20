import pytest

from src.core.entities.release import Release
from src.core.use_cases.v2.pipeline.upsert_release import UpsertRelease


@pytest.fixture
def repo():
    from tests.mock.repositories_async.mock_async_release_repository import (
        MockAsyncReleaseRepository,
    )
    return MockAsyncReleaseRepository()


@pytest.fixture
def use_case(repo):
    return UpsertRelease(repo)


@pytest.mark.asyncio
async def test_upsert_release_create(use_case, repo):
    initial_count = len(repo.releases)
    new_release = Release(
        id="new-release-id",
        title="New Release",
        url="https://example.com/new.pdf",
        filename="new.pdf",
        year=2026,
        page_count=10,
    )
    result, was_created = await use_case.execute(new_release)
    assert result.id == "new-release-id"
    assert result.title == "New Release"
    assert was_created is True
    assert len(repo.releases) == initial_count + 1


@pytest.mark.asyncio
async def test_upsert_release_update(use_case, repo):
    initial_count = len(repo.releases)
    updated_release = Release(
        id="id_2024",
        title="Updated Title",
        url="https://example.com/updated.pdf",
        filename="updated.pdf",
        year=2024,
        page_count=99,
    )
    result, was_created = await use_case.execute(updated_release)
    assert result.id == "id_2024"
    assert result.title == "Updated Title"
    assert result.page_count == 99
    assert was_created is False
    assert len(repo.releases) == initial_count


@pytest.mark.asyncio
async def test_upsert_release_update_all_fields(use_case, repo):
    updated = Release(
        id="id_2025",
        title="New Title",
        url="https://example.com/new.pdf",
        filename="new.pdf",
        year=2025,
        page_count=50,
    )
    result, was_created = await use_case.execute(updated)
    assert result.title == "New Title"
    assert result.url == "https://example.com/new.pdf"
    assert result.filename == "new.pdf"
    assert result.year == 2025
    assert result.page_count == 50
    assert was_created is False
