import pytest

from src.core.use_cases.v1.release.get_release_by_id import GetReleaseById

RELEASE_ID = "id_2024"


@pytest.fixture
def repo():
    from tests.mock.repositories.mock_release_repository import (
        MockReleaseRepository,
    )

    return MockReleaseRepository()


@pytest.fixture
def use_case(repo):
    from src.core.use_cases.v1.release.get_release_by_id import GetReleaseById

    return GetReleaseById(repo)


def test_get_release_by_id(use_case: GetReleaseById):
    release = use_case.execute(RELEASE_ID)
    assert release.id == RELEASE_ID


def test_get_release_by_id_not_found(use_case: GetReleaseById):
    with pytest.raises(ValueError) as exc_info:
        use_case.execute("nonexistent-id")
    assert str(exc_info.value) == "Release with ID nonexistent-id not found."


def test_get_release_by_id_empty_string(use_case: GetReleaseById):
    with pytest.raises(ValueError) as exc_info:
        use_case.execute("")
    assert str(exc_info.value) == "Release with ID  not found."


def test_get_release_by_id_upper_case(use_case: GetReleaseById):
    release = use_case.execute(RELEASE_ID.upper())
    assert release.id == RELEASE_ID


def test_get_release_by_id_leading_trailing_spaces(use_case: GetReleaseById):
    release = use_case.execute(f" {RELEASE_ID} ")
    assert release.id == RELEASE_ID
