from src.core.interfaces.allocation_repository import AllocationRepository


class ListAllocationsByAgency:
    def __init__(self, allocation_repository: AllocationRepository):
        self.allocation_repository = allocation_repository

    def execute(self, agency: str, cursor: int, limit: int):
        return self.allocation_repository.list_allocations_by_agency(
            agency, cursor, limit
        )
