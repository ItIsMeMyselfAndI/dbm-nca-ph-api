import pytest


@pytest.fixture
def repo():
    from tests.mock.repositories.mock_release_repository import (
        MockReleaseRepository,
    )

    return MockReleaseRepository()


@pytest.fixture
def use_case(repo):
    from src.core.use_cases.release.get_release_by_id import GetReleaseById

    return GetReleaseById(repo)


def test_get_release_by_id(use_case):
    release = use_case.execute("id_2024")
    assert release.id == "id_2024"


def test_get_release_by_id_not_found(use_case):
    with pytest.raises(ValueError) as exc_info:
        use_case.execute("nonexistent-id")
    assert str(exc_info.value) == "Release with ID nonexistent-id not found."


def test_get_release_by_id_empty_string(use_case):
    with pytest.raises(ValueError) as exc_info:
        use_case.execute("")
    assert str(exc_info.value) == "Release with ID  not found."


def test_get_release_by_id_upper_case(use_case):
    release = use_case.execute("ID_2024")
    assert release.id == "id_2024"


def test_get_release_by_id_leading_trailing_spaces(use_case):
    release = use_case.execute(" id_2024 ")
    assert release.id == "id_2024"
