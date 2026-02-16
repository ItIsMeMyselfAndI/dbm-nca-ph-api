import pytest

from src.core.entities.record import Record


def test_record():
    record = Record(
        id="1",
        nca_number="NCA-123",
        nca_type="Type A",
        released_date="2024-01-01",
        department="Department X",
        purpose="Purpose Y",
        release_id="release_2024",
    )

    assert record.id == "1"
    assert record.nca_number == "NCA-123"
    assert record.nca_type == "Type A"
    assert record.released_date == "2024-01-01"
    assert record.department == "Department X"
    assert record.purpose == "Purpose Y"
    assert record.release_id == "release_2024"


def test_record_missing_fields():
    with pytest.raises(ValueError) as exc_info:
        record = Record(  # pyright: ignore
            id="2",
            nca_number="NCA-124",
            nca_type="Type B",
            released_date="2024-02-01",
            department="Department Y",
            purpose="Purpose Z",
        )
    print(exc_info.value)


def test_record_non_string_id():
    with pytest.raises(ValueError) as exc_info:
        record = Record(
            id=2,  # pyright: ignore
            nca_number="NCA-125",
            nca_type="Type C",
            released_date="2024-03-01",
            department="Department Z",
            purpose="Purpose A",
            release_id="release_2025",
        )
    print(exc_info.value)


def test_record_non_string_nca_number():
    with pytest.raises(ValueError) as exc_info:
        record = Record(
            id="3",
            nca_number=125,  # pyright: ignore
            nca_type="Type D",
            released_date="2024-04-01",
            department="Department A",
            purpose="Purpose B",
            release_id="release_2026",
        )
    print(exc_info.value)


def test_record_non_string_nca_type():
    with pytest.raises(ValueError) as exc_info:
        record = Record(
            id="8",
            nca_number="NCA-130",
            nca_type=789,  # pyright: ignore
            released_date="2024-08-01",
            department="Department E",
            purpose="Purpose F",
            release_id="release_2031",
        )
    print(exc_info.value)


def test_record_non_string_released_date():
    with pytest.raises(ValueError) as exc_info:
        record = Record(
            id="5",
            nca_number="NCA-127",
            nca_type="Type F",
            released_date=20240601,  # pyright: ignore
            department="Department C",
            purpose="Purpose D",
            release_id="release_2028",
        )
    print(exc_info.value)


def test_record_non_string_department():
    with pytest.raises(ValueError) as exc_info:
        record = Record(
            id="6",
            nca_number="NCA-128",
            nca_type="Type G",
            released_date="2024-06-01",
            department=123,  # pyright: ignore
            purpose="Purpose E",
            release_id="release_2029",
        )
    print(exc_info.value)


def test_record_non_string_purpose():
    with pytest.raises(ValueError) as exc_info:
        record = Record(
            id="7",
            nca_number="NCA-129",
            nca_type="Type H",
            released_date="2024-07-01",
            department="Department D",
            purpose=456,  # pyright: ignore
            release_id="release_2030",
        )
    print(exc_info.value)


def test_record_non_string_release_id():
    with pytest.raises(ValueError) as exc_info:
        record = Record(
            id="4",
            nca_number="NCA-126",
            nca_type="Type E",
            released_date="2024-05-01",
            department="Department B",
            purpose="Purpose C",
            release_id=2027,  # pyright: ignore
        )
    print(exc_info.value)
