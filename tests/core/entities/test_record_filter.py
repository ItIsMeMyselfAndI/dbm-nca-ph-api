from src.core.entities.record_filter import RecordFilter


def test_record_filter():
    assert RecordFilter.DEPARTMENT.value == "department"
    assert RecordFilter.NCA_TYPE.value == "nca_type"
    assert RecordFilter.RELEASE_ID.value == "release_id"
    assert RecordFilter.RELEASED_DATE.value == "released_date"


def test_record_filter_enum():
    assert isinstance(RecordFilter.DEPARTMENT, RecordFilter)
    assert isinstance(RecordFilter.NCA_TYPE, RecordFilter)
    assert isinstance(RecordFilter.RELEASE_ID, RecordFilter)
    assert isinstance(RecordFilter.RELEASED_DATE, RecordFilter)


def test_record_filter_enum_values():
    assert RecordFilter("department") == RecordFilter.DEPARTMENT
    assert RecordFilter("nca_type") == RecordFilter.NCA_TYPE
    assert RecordFilter("release_id") == RecordFilter.RELEASE_ID
    assert RecordFilter("released_date") == RecordFilter.RELEASED_DATE


def test_record_filter_invalid_value():
    try:
        RecordFilter("invalid_value")
    except ValueError as e:
        assert str(e) == "'invalid_value' is not a valid RecordFilter"


def test_record_filter_enum_members():
    members = list(RecordFilter)
    assert len(members) == 4
    assert RecordFilter.DEPARTMENT in members
    assert RecordFilter.NCA_TYPE in members
    assert RecordFilter.RELEASE_ID in members
    assert RecordFilter.RELEASED_DATE in members


def test_record_filter_enum_str():
    assert str(RecordFilter.DEPARTMENT) == "RecordFilter.DEPARTMENT"
    assert str(RecordFilter.NCA_TYPE) == "RecordFilter.NCA_TYPE"
    assert str(RecordFilter.RELEASE_ID) == "RecordFilter.RELEASE_ID"
    assert str(RecordFilter.RELEASED_DATE) == "RecordFilter.RELEASED_DATE"


def test_record_filter_enum_comparison():
    assert RecordFilter.DEPARTMENT == RecordFilter.DEPARTMENT
    assert RecordFilter.NCA_TYPE == RecordFilter.NCA_TYPE
    assert RecordFilter.RELEASE_ID == RecordFilter.RELEASE_ID
    assert RecordFilter.RELEASED_DATE == RecordFilter.RELEASED_DATE
    assert RecordFilter.DEPARTMENT != RecordFilter.NCA_TYPE
    assert RecordFilter.DEPARTMENT != RecordFilter.RELEASE_ID
    assert RecordFilter.DEPARTMENT != RecordFilter.RELEASED_DATE
    assert RecordFilter.NCA_TYPE != RecordFilter.RELEASE_ID
    assert RecordFilter.NCA_TYPE != RecordFilter.RELEASED_DATE
    assert RecordFilter.RELEASE_ID != RecordFilter.RELEASED_DATE


def test_record_filter_enum_iteration():
    members = list(RecordFilter)
    assert len(members) == 4
    assert RecordFilter.DEPARTMENT in members
    assert RecordFilter.NCA_TYPE in members
    assert RecordFilter.RELEASE_ID in members
    assert RecordFilter.RELEASED_DATE in members


def test_record_filter_enum_name():
    assert RecordFilter.DEPARTMENT.name == "DEPARTMENT"
    assert RecordFilter.NCA_TYPE.name == "NCA_TYPE"
    assert RecordFilter.RELEASE_ID.name == "RELEASE_ID"
    assert RecordFilter.RELEASED_DATE.name == "RELEASED_DATE"
