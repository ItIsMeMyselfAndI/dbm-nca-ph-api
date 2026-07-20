import pytest

pytestmark = pytest.mark.asyncio


async def test_get_release_by_id(client, seed_releases):
    response = client.get("/releases/test_release_a")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == "test_release_a"


async def test_get_release_by_id_not_found(client, seed_releases):
    response = client.get("/releases/nonexistent-id")
    assert response.status_code == 404


async def test_get_release_by_id_in_upper_case(client, seed_releases):
    response = client.get("/releases/TEST_RELEASE_A")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == "test_release_a"


async def test_get_release_by_id_leading_trailing_spaces(client, seed_releases):
    response = client.get("/releases/ test_release_a ")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == "test_release_a"
