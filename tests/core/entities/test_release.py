import pytest
from src.core.entities.release import Release


def test_release():
    release = Release(
        id="id_2024",
        title="NCA 2024",
        url="https://www.dbm.gov.ph/wp-content/uploads/NCA/2024/NCA_2024.pdf",
        filename="NCA_2024.pdf",
        year=2024,
        page_count=100,
        file_meta_created_at="2024-01-01T00:00:00Z",
        file_meta_modified_at="2024-01-02T00:00:00Z",
    )

    assert release.id == "id_2024"
    assert release.title == "NCA 2024"
    assert (
        release.url == "https://www.dbm.gov.ph/wp-content/uploads/NCA/2024/NCA_2024.pdf"
    )
    assert release.filename == "NCA_2024.pdf"
    assert release.year == 2024
    assert release.page_count == 100
    assert release.file_meta_created_at == "2024-01-01T00:00:00Z"
    assert release.file_meta_modified_at == "2024-01-02T00:00:00Z"


def test_release_missing_fields():
    with pytest.raises(ValueError) as exc_info:
        release = Release(  # pyright: ignore
            id="id_2025",
            title="NCA 2025",
            url="https://www.dbm.gov.ph/wp-content/uploads/NCA/2025/NCA_2025.pdf",
            filename="NCA_2025.pdf",
        )
    print(exc_info.value)


def test_release_non_string_id():
    with pytest.raises(ValueError) as exc_info:
        release = Release(
            id=123,  # pyright: ignore
            title="NCA 2026",
            url="https://www.dbm.gov.ph/wp-content/uploads/NCA/2026/NCA_2026.pdf",
            filename="NCA_2026.pdf",
            year=2026,
        )
    print(exc_info.value)


def test_release_non_string_title():
    with pytest.raises(ValueError) as exc_info:
        release = Release(
            id="id_2027",
            title=456,  # pyright: ignore
            url="https://www.dbm.gov.ph/wp-content/uploads/NCA/2027/NCA_2027.pdf",
            filename="NCA_2027.pdf",
            year=2027,
        )
    print(exc_info.value)


def test_release_non_string_url():
    with pytest.raises(ValueError) as exc_info:
        release = Release(
            id="id_2028",
            title="NCA 2028",
            url=789,  # pyright: ignore
            filename="NCA_2028.pdf",
            year=2028,
        )
    print(exc_info.value)


def test_release_non_string_filename():
    with pytest.raises(ValueError) as exc_info:
        release = Release(
            id="id_2029",
            title="NCA 2029",
            url="https://www.dbm.gov.ph/wp-content/uploads/NCA/2029/NCA_2029.pdf",
            filename=101112,  # pyright: ignore
            year=2029,
        )
    print(exc_info.value)


def test_release_non_integer_year():
    with pytest.raises(ValueError) as exc_info:
        release = Release(
            id="id_2030",
            title="NCA 2030",
            url="https://www.dbm.gov.ph/wp-content/uploads/NCA/2030/NCA_2030.pdf",
            filename="NCA_2030.pdf",
            year="lakjfdk",  # pyright: ignore
        )
    print(exc_info.value)


def test_release_non_integer_page_count():
    with pytest.raises(ValueError) as exc_info:
        release = Release(
            id="id_2031",
            title="NCA 2031",
            url="https://www.dbm.gov.ph/wp-content/uploads/NCA/2031/NCA_2031.pdf",
            filename="NCA_2031.pdf",
            year=2031,
            page_count="lsadj",  # pyright: ignore
        )
    print(exc_info.value)


def test_release_non_string_file_meta_created_at():
    with pytest.raises(ValueError) as exc_info:
        release = Release(
            id="id_2032",
            title="NCA 2032",
            url="https://www.dbm.gov.ph/wp-content/uploads/NCA/2032/NCA_2032.pdf",
            filename="NCA_2032.pdf",
            year=2032,
            file_meta_created_at=123,  # pyright: ignore
        )
    print(exc_info.value)


def test_release_non_string_file_meta_modified_at():
    with pytest.raises(ValueError) as exc_info:
        release = Release(
            id="id_2033",
            title="NCA 2033",
            url="https://www.dbm.gov.ph/wp-content/uploads/NCA/2033/NCA_2033.pdf",
            filename="NCA_2033.pdf",
            year=2033,
            file_meta_modified_at=456,  # pyright: ignore
        )
    print(exc_info.value)
