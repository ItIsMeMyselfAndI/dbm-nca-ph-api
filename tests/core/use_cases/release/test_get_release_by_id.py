import pytest


@pytest.fixture
def repo():
    from tests.infrastructure.db.mock_release_repository import (
        MockReleaseRepository,
    )

    return MockReleaseRepository()


def test_get_release_by_id(repo):
    release = repo.get_release_by_id("id_2024")
    assert release is not None
    assert release.id == "id_2024"
    assert release.year == 2024
    assert (
        release.url == "https://www.dbm.gov.ph/wp-content/uploads/NCA/2024/NCA_2024.pdf"
    )
    assert release.filename == "NCA_2024.pdf"


def test_get_release_by_id_not_found(repo):
    with pytest.raises(ValueError) as exc_info:
        repo.get_release_by_id("nonexistent-id")
    assert str(exc_info.value) == "Release with ID nonexistent-id not found."


def test_get_release_by_id_empty_string(repo):
    with pytest.raises(ValueError) as exc_info:
        repo.get_release_by_id("")
    assert str(exc_info.value) == "Release with ID  not found."


def test_get_release_by_id_none(repo):
    with pytest.raises(ValueError) as exc_info:
        repo.get_release_by_id(None)
    assert str(exc_info.value) == "Release with ID None not found."


def test_get_release_by_id_case_sensitivity(repo):
    with pytest.raises(ValueError) as exc_info:
        repo.get_release_by_id("ID_2024")
    assert str(exc_info.value) == "Release with ID ID_2024 not found."


def test_get_release_by_id_leading_trailing_spaces(repo):
    with pytest.raises(ValueError) as exc_info:
        repo.get_release_by_id(" id_2024 ")
    assert str(exc_info.value) == "Release with ID  id_2024  not found."
