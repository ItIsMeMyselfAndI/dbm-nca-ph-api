from typing import Dict
from src.core.interfaces.allocation_repository import AllocationRepository


class ListAllocations:
    def __init__(self, allocation_repository: AllocationRepository):
        self.allocation_repository = allocation_repository

    def execute(self, cursor: int, limit: int, filter: Dict[str, str] | None = None):
        if not filter:
            return self.allocation_repository.list_allocations(cursor, limit)

        key, value = next(iter(filter.items()))

        if key == "agency":
            return self.allocation_repository.list_allocations_by_agency(
                value, cursor, limit
            )
        elif key == "nca_number":
            return self.allocation_repository.list_allocations_by_nca_number(
                value, cursor, limit
            )
        elif key == "operating_unit":
            return self.allocation_repository.list_allocations_by_operating_unit(
                value, cursor, limit
            )
        else:
            raise ValueError(f"Unsupported filter key: {key}")
