from src.core.interfaces.allocation_repository import AllocationRepository


class ListAllocationsByNCANumber:
    def __init__(self, allocation_repository: AllocationRepository):
        self.allocation_repository = allocation_repository

    def execute(self, nca_number: str, cursor: int, limit: int):
        return self.allocation_repository.list_allocations_by_nca_number(
            nca_number, cursor, limit
        )
