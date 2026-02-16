from src.core.entities.allocation_filter import AllocationFilter


def test_allocation_filter():
    assert AllocationFilter.AGENCY.value == "agency"
    assert AllocationFilter.NCA_NUMBER.value == "nca_number"
    assert AllocationFilter.OPERATING_UNIT.value == "operating_unit"


def test_allocation_filter_enum():
    assert isinstance(AllocationFilter.AGENCY, AllocationFilter)
    assert isinstance(AllocationFilter.NCA_NUMBER, AllocationFilter)
    assert isinstance(AllocationFilter.OPERATING_UNIT, AllocationFilter)


def test_allocation_filter_enum_values():
    assert AllocationFilter("agency") == AllocationFilter.AGENCY
    assert AllocationFilter("nca_number") == AllocationFilter.NCA_NUMBER
    assert AllocationFilter("operating_unit") == AllocationFilter.OPERATING_UNIT


def test_allocation_filter_invalid_value():
    try:
        AllocationFilter("invalid_value")
    except ValueError as e:
        assert str(e) == "'invalid_value' is not a valid AllocationFilter"


def test_allocation_filter_enum_members():
    members = list(AllocationFilter)
    assert len(members) == 3
    assert AllocationFilter.AGENCY in members
    assert AllocationFilter.NCA_NUMBER in members
    assert AllocationFilter.OPERATING_UNIT in members


def test_allocation_filter_enum_str():
    assert str(AllocationFilter.AGENCY) == "AllocationFilter.AGENCY"
    assert str(AllocationFilter.NCA_NUMBER) == "AllocationFilter.NCA_NUMBER"
    assert str(AllocationFilter.OPERATING_UNIT) == "AllocationFilter.OPERATING_UNIT"


def test_allocation_filter_enum_comparison():
    assert AllocationFilter.AGENCY == AllocationFilter.AGENCY
    assert AllocationFilter.NCA_NUMBER == AllocationFilter.NCA_NUMBER
    assert AllocationFilter.OPERATING_UNIT == AllocationFilter.OPERATING_UNIT
    assert AllocationFilter.AGENCY != AllocationFilter.NCA_NUMBER
    assert AllocationFilter.AGENCY != AllocationFilter.OPERATING_UNIT
    assert AllocationFilter.NCA_NUMBER != AllocationFilter.OPERATING_UNIT


def test_allocation_filter_enum_iteration():
    filters = [filter for filter in AllocationFilter]
    assert filters == [
        AllocationFilter.AGENCY,
        AllocationFilter.NCA_NUMBER,
        AllocationFilter.OPERATING_UNIT,
    ]


def test_allocation_filter_enum_name():
    assert AllocationFilter.AGENCY.name == "AGENCY"
    assert AllocationFilter.NCA_NUMBER.name == "NCA_NUMBER"
    assert AllocationFilter.OPERATING_UNIT.name == "OPERATING_UNIT"
