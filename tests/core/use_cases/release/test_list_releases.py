import pytest


@pytest.fixture
def repo():
    from tests.infrastructure.db.mock_release_repository import (
        MockReleaseRepository,
    )

    return MockReleaseRepository()


def test_list_releases(repo):
    releases = repo.list_releases(limit=10)
    assert len(releases) == 3
    assert releases[0].id == "id_2024"
    assert releases[0].year == 2024
    assert (
        releases[0].url
        == "https://www.dbm.gov.ph/wp-content/uploads/NCA/2024/NCA_2024.pdf"
    )
    assert releases[0].filename == "NCA_2024.pdf"


def test_list_releases_with_cursor(repo):
    first_page = repo.list_releases(limit=2)
    assert len(first_page) == 2
    assert first_page[0].id == "id_2024"

    second_page = repo.list_releases(limit=2, cursor=first_page[-1].id)
    assert len(second_page) == 1
    assert second_page[0].id == "id_2026"


def test_list_releases_with_invalid_cursor(repo):
    with pytest.raises(ValueError) as exc_info:
        repo.list_releases(limit=2, cursor="nonexistent-id")
    assert str(exc_info.value) == "Cursor with ID nonexistent-id not found."


def test_list_releases_with_empty_cursor(repo):
    with pytest.raises(ValueError) as exc_info:
        repo.list_releases(limit=2, cursor="")
    assert str(exc_info.value) == "Cursor with ID  not found."


def test_list_releases_with_none_cursor(repo):
    with pytest.raises(ValueError) as exc_info:
        repo.list_releases(limit=2, cursor=None)
    assert str(exc_info.value) == "Cursor with ID None not found."


def test_list_releases_with_leading_trailing_spaces_cursor(repo):
    with pytest.raises(ValueError) as exc_info:
        repo.list_releases(limit=2, cursor=" id_2024 ")
    assert str(exc_info.value) == "Cursor with ID  id_2024  not found."


def test_list_releases_with_case_sensitivity_cursor(repo):
    with pytest.raises(ValueError) as exc_info:
        repo.list_releases(limit=2, cursor="ID_2024")
    assert str(exc_info.value) == "Cursor with ID ID_2024 not found."


def test_list_releases_with_limit_zero(repo):
    releases = repo.list_releases(limit=0)
    assert len(releases) == 0


def test_list_releases_with_limit_exceeding_total(repo):
    releases = repo.list_releases(limit=10)
    assert len(releases) == 3


def test_list_releases_with_negative_limit(repo):
    with pytest.raises(ValueError) as exc_info:
        repo.list_releases(limit=-5)
    assert str(exc_info.value) == "Limit must be a non-negative integer."
