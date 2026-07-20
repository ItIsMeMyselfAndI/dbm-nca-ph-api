import pytest

pytestmark = pytest.mark.asyncio


async def test_list_releases(client, seed_releases):
    response = client.get("/releases?limit=10")
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert data["count"] == 3
    assert data["cursor"] is None
    assert data["next_cursor"] == "test_release_c"


async def test_list_releases_with_cursor(client, seed_releases):
    response = client.get("/releases?limit=2")
    assert response.status_code == 200
    data = response.json()
    assert data["count"] == 2
    assert data["next_cursor"] is not None

    response_next = client.get(f"/releases?limit=2&cursor={data['next_cursor']}")
    assert response_next.status_code == 200
    data_next = response_next.json()
    assert data_next["count"] == 1
    assert data_next["cursor"] == data["next_cursor"]


async def test_list_releases_with_invalid_cursor(client, seed_releases):
    response = client.get("/releases?limit=2&cursor=nonexistent-id")
    assert response.status_code == 200
    data = response.json()
    assert data["count"] == 2
    assert data["cursor"] == "nonexistent-id"


async def test_list_releases_with_empty_cursor(client, seed_releases):
    response = client.get("/releases?limit=2&cursor=")
    assert response.status_code == 400


async def test_list_releases_with_limit_zero(client, seed_releases):
    response = client.get("/releases?limit=0")
    assert response.status_code == 200
    data = response.json()
    assert data["count"] == 0
    assert data["cursor"] is None
    assert data["next_cursor"] is None


async def test_list_releases_with_negative_limit(client, seed_releases):
    response = client.get("/releases?limit=-5")
    assert response.status_code == 200
    data = response.json()
    assert data["count"] == 0
    assert data["cursor"] is None
    assert data["next_cursor"] is None


async def test_list_releases_with_leading_trailing_spaces_cursor(
    client, seed_releases
):
    response = client.get("/releases?limit=2&cursor= test_release_a ")
    assert response.status_code == 200
    data = response.json()
    assert data["count"] == 2
    assert data["cursor"] is not None
    assert data["next_cursor"] is not None


async def test_list_releases_with_upper_case_cursor(client, seed_releases):
    response = client.get("/releases?limit=2&cursor=TEST_RELEASE_A")
    assert response.status_code == 200
    data = response.json()
    assert data["count"] == 2
    assert data["cursor"] is not None
    assert data["next_cursor"] is not None


async def test_list_releases_with_limit_exceeding_total(client, seed_releases):
    response = client.get("/releases?limit=10")
    assert response.status_code == 200
    data = response.json()
    assert data["count"] == 3
    assert data["cursor"] is None
    assert data["next_cursor"] == "test_release_c"
