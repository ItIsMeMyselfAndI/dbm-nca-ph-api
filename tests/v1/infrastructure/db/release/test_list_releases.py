import pytest


@pytest.fixture
def repo():
    from tests.mock.repositories.mock_release_repository import (
        MockReleaseRepository,
    )

    return MockReleaseRepository()


def test_list_releases(repo):
    releases = repo.list_releases(limit=10)
    assert len(releases) == 3


def test_list_releases_with_cursor(repo):
    first_page = repo.list_releases(limit=2)
    assert len(first_page) == 2

    second_page = repo.list_releases(limit=2, cursor=first_page[-1].id)
    assert len(second_page) == 1


def test_list_releases_with_invalid_cursor(repo):
    with pytest.raises(ValueError) as exc_info:
        repo.list_releases(limit=2, cursor="nonexistent-id")
    assert str(exc_info.value) == "Cursor with ID nonexistent-id not found."


def test_list_releases_with_empty_cursor(repo):
    releases = repo.list_releases(limit=2, cursor="")
    assert len(releases) == 2


def test_list_releases_with_none_cursor(repo):
    releases = repo.list_releases(limit=2, cursor=None)
    assert len(releases) == 2


def test_list_releases_with_leading_trailing_spaces_cursor(repo):
    releases = repo.list_releases(limit=2, cursor=" id_2024 ")
    assert len(releases) == 2


def test_list_releases_with_upper_case_cursor(repo):
    releases = repo.list_releases(limit=2, cursor="ID_2024")
    assert len(releases) == 2


def test_list_releases_with_limit_zero(repo):
    releases = repo.list_releases(limit=0)
    assert len(releases) == 0


def test_list_releases_with_limit_exceeding_total(repo):
    releases = repo.list_releases(limit=10)
    assert len(releases) == 3


def test_list_releases_with_negative_limit(repo):
    releases = repo.list_releases(limit=-5)
    assert len(releases) == 0
