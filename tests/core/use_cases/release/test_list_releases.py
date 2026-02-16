import pytest


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


def test_list_releases(use_case):
    releases, next_cursor = use_case.execute(limit=10)
    assert len(releases) == 3
    assert next_cursor is None


def test_list_releases_with_cursor(use_case):
    releases, next_cursor = use_case.execute(limit=2)
    assert len(releases) == 2
    assert next_cursor is not None

    releases_next, next_cursor_next = use_case.execute(limit=2, cursor=next_cursor)
    assert len(releases_next) == 1
    assert next_cursor_next is None


def test_list_releases_with_invalid_cursor(use_case):
    with pytest.raises(ValueError) as exc_info:
        use_case.execute(limit=2, cursor="nonexistent-id")
    assert str(exc_info.value) == "Cursor with ID nonexistent-id not found."


def test_list_releases_with_empty_cursor(use_case):
    with pytest.raises(ValueError) as exc_info:
        use_case.execute(limit=2, cursor="")
    assert str(exc_info.value) == "Cursor cannot be an empty string."


def test_list_releases_with_leading_trailing_spaces_cursor(use_case):
    releases, next_cursor = use_case.execute(limit=2, cursor=" id_2024 ")
    assert len(releases) == 2
    assert next_cursor is not None


def test_list_releases_with_upper_case_cursor(use_case):
    releases, next_cursor = use_case.execute(limit=2, cursor="ID_2024")
    assert len(releases) == 2
    assert next_cursor is not None


def test_list_releases_with_limit_zero(use_case):
    releases, next_cursor = use_case.execute(limit=0)
    assert len(releases) == 0
    assert next_cursor is None


def test_list_releases_with_limit_exceeding_total(use_case):
    releases, next_cursor = use_case.execute(limit=10)
    assert len(releases) == 3
    assert next_cursor is None


def test_list_releases_with_negative_limit(use_case):
    releases, next_cursor = use_case.execute(limit=-5)
    assert len(releases) == 0
    assert next_cursor is None
