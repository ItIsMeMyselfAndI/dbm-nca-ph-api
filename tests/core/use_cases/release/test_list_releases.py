import pytest

from src.core.use_cases.release.list_releases import ListReleases

RELEASE_ID = "id_2024"
LIMIT_ROW_COUNT = 2


@pytest.fixture
def repo():
    from tests.mock.repositories.mock_release_repository import (
        MockReleaseRepository,
    )

    return MockReleaseRepository()


@pytest.fixture
def use_case(repo):
    from src.core.use_cases.release.list_releases import ListReleases

    return ListReleases(repo)


def test_list_releases(use_case: ListReleases):
    releases, next_cursor = use_case.execute(limit=LIMIT_ROW_COUNT)
    assert len(releases) <= LIMIT_ROW_COUNT
    if len(releases) != 0:
        assert next_cursor == releases[-1].id


def test_list_releases_with_cursor(use_case: ListReleases):
    releases, next_cursor = use_case.execute(limit=LIMIT_ROW_COUNT)
    assert len(releases) <= LIMIT_ROW_COUNT
    if len(releases) != 0:
        assert next_cursor == releases[-1].id

    releases_next, next_cursor_next = use_case.execute(
        limit=LIMIT_ROW_COUNT, cursor=next_cursor
    )
    assert len(releases_next) <= LIMIT_ROW_COUNT
    if len(releases_next) != 0:
        assert next_cursor_next == releases_next[-1].id


def test_list_releases_with_invalid_cursor(use_case: ListReleases):
    with pytest.raises(ValueError) as exc_info:
        use_case.execute(limit=LIMIT_ROW_COUNT, cursor="nonexistent-id")
    assert str(exc_info.value) == "Cursor with ID nonexistent-id not found."


def test_list_releases_with_empty_cursor(use_case: ListReleases):
    with pytest.raises(ValueError) as exc_info:
        use_case.execute(limit=LIMIT_ROW_COUNT, cursor="")
    assert str(exc_info.value) == "Cursor cannot be an empty string."


def test_list_releases_with_leading_trailing_spaces_cursor(use_case: ListReleases):
    releases, next_cursor = use_case.execute(
        limit=LIMIT_ROW_COUNT, cursor=f" {RELEASE_ID} "
    )
    assert len(releases) <= LIMIT_ROW_COUNT
    if len(releases) != 0:
        assert next_cursor == releases[-1].id


def test_list_releases_with_upper_case_cursor(use_case: ListReleases):
    releases, next_cursor = use_case.execute(
        limit=LIMIT_ROW_COUNT, cursor=RELEASE_ID.upper()
    )
    assert len(releases) <= LIMIT_ROW_COUNT
    if len(releases) != 0:
        assert next_cursor == releases[-1].id


def test_list_releases_with_limit_zero(use_case: ListReleases):
    releases, next_cursor = use_case.execute(limit=0)
    assert len(releases) == 0
    assert next_cursor is None


def test_list_releases_with_negative_limit(use_case: ListReleases):
    releases, next_cursor = use_case.execute(limit=-5)
    assert len(releases) == 0
    assert next_cursor is None
