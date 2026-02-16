from typing import Dict, List, Tuple

from src.core.entities.allocation import Allocation
from src.core.entities.allocation_filter import AllocationFilter
from src.core.interfaces.allocation_repository import AllocationRepository


class ListAllocationsByFilter:
    def __init__(self, allocation_repository: AllocationRepository):
        self.allocation_repository = allocation_repository

    def execute(
        self, limit: int, filter: Dict[AllocationFilter, str], cursor: str | None = None
    ) -> Tuple[List[Allocation], str | None]:
        if limit <= 0:
            return [], None

        try:
            if cursor is not None:
                self.allocation_repository.get_allocation_by_id(cursor)
        except ValueError:
            raise ValueError(f"Cursor with ID {cursor} not found.")

        allocations = self.allocation_repository.list_allocations_by_filter(
            limit, filter, cursor
        )
        if len(allocations) < limit:
            next_cursor = None
        else:
            next_cursor = allocations[-1].id
        return allocations, next_cursor
