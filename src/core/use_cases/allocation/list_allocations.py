from typing import List, Tuple

from src.core.entities.allocation import Allocation
from src.core.interfaces.allocation_repository import AllocationRepository


class ListAllocations:
    def __init__(self, allocation_repository: AllocationRepository):
        self.allocation_repository = allocation_repository

    def execute(
        self, limit: int, cursor: str | None = None
    ) -> Tuple[List[Allocation], str | None]:
        if limit <= 0:
            return [], None

        allocations = self.allocation_repository.list_allocations(limit, cursor)
        if len(allocations) < limit:
            next_cursor = None
        else:
            next_cursor = allocations[-1].id
        return allocations, next_cursor
