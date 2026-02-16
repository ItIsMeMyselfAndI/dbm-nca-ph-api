import pytest


@pytest.fixture
def repo():
    from tests.mock.repositories.mock_release_repository import (
        MockReleaseRepository,
    )

    return MockReleaseRepository()


def test_get_release_by_id(repo):
    release = repo.get_release_by_id("id_2024")
    assert release is not None
    assert release.id == "id_2024"


def test_get_release_by_id_not_found(repo):
    with pytest.raises(ValueError) as exc_info:
        repo.get_release_by_id("nonexistent-id")
    assert str(exc_info.value) == "Release with ID nonexistent-id not found."


def test_get_release_by_id_empty_string(repo):
    with pytest.raises(ValueError) as exc_info:
        repo.get_release_by_id("")
    assert str(exc_info.value) == "Release with ID  not found."


# def test_get_release_by_id_none(repo):
#     with pytest.raises(ValueError) as exc_info:
#         repo.get_release_by_id(None)
#     assert str(exc_info.value) == "Release with ID None not found."


def test_get_release_by_id_in_upper_case(repo):
    release = repo.get_release_by_id("ID_2024")
    assert release is not None
    assert release.id == "id_2024"


def test_get_release_by_id_leading_trailing_spaces(repo):
    release = repo.get_release_by_id(" id_2024 ")
    assert release is not None
    assert release.id == "id_2024"
