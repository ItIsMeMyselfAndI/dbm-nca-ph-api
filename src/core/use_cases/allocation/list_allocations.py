from core.interfaces.allocation_repository import AllocationRepository


class ListAllocations:
    def __init__(self, allocation_repository: AllocationRepository):
        self.allocation_repository = allocation_repository

    def execute(self, cursor: int, limit: int):
        return self.allocation_repository.list_allocations(cursor, limit)
