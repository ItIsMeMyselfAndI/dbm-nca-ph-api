from core.interfaces.allocation_repository import AllocationRepository


class ListAllocationsByOperatingUnit:
    def __init__(self, allocation_repository: AllocationRepository):
        self.allocation_repository = allocation_repository

    def execute(self, operating_unit: str, cursor: int, limit: int):
        return self.allocation_repository.list_allocations_by_operating_unit(
            operating_unit, cursor, limit
        )
