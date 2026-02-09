from typing import List, Tuple
from src.core.domain.allocation import Allocation
from src.core.interfaces.allocation_repository import AllocationRepository


class ListAllocations:
    def __init__(self, allocation_repository: AllocationRepository):
        self.allocation_repository = allocation_repository

    def execute(
        self, limit: int, cursor: str | None = None
    ) -> Tuple[List[Allocation], str | None]:
        allocations = self.allocation_repository.list_allocations(limit + 1, cursor)
        has_more = len(allocations) == limit + 1

        next_cursor = allocations[-1].id if has_more else None
        relevant_allocations = allocations[: limit + 1]
        return relevant_allocations, next_cursor
