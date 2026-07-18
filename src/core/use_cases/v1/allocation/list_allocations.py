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

        if cursor == "":
            raise ValueError("Cursor cannot be an empty string.")

        try:
            if cursor is not None:
                self.allocation_repository.get_allocation_by_id(cursor)
        except ValueError:
            raise ValueError(f"Cursor with ID {cursor} not found.")

        allocations = self.allocation_repository.list_allocations(limit, cursor)
        if len(allocations) == 0:
            next_cursor = None
        else:
            next_cursor = allocations[-1].id
        return allocations, next_cursor
