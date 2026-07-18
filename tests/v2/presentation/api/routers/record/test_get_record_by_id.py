def test_get_record_by_id(client):
    response = client.get("/records/a729caee-c88f-416b-ba35-fca60a553aaa")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == "a729caee-c88f-416b-ba35-fca60a553aaa"


def test_get_record_by_id_not_found(client):
    response = client.get("/records/nonexistent-id")
    assert response.status_code == 404


def test_get_record_by_id_in_upper_case(client):
    response = client.get("/records/A729CAEE-C88F-416B-BA35-FCA60A553AAA")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == "a729caee-c88f-416b-ba35-fca60a553aaa"


def test_get_record_by_id_leading_trailing_spaces(client):
    response = client.get("/records/ a729caee-c88f-416b-ba35-fca60a553aaa ")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == "a729caee-c88f-416b-ba35-fca60a553aaa"
