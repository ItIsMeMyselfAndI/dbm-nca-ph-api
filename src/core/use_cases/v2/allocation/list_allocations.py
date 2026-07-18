from typing import List, Tuple

from src.core.entities.allocation import Allocation
from src.core.exceptions import ValidationError
from src.core.interfaces.async_allocation_repository import AsyncAllocationRepository
from src.core.use_cases.v2._cursor import compute_next_cursor


class ListAllocations:
    def __init__(self, allocation_repository: AsyncAllocationRepository):
        self.allocation_repository = allocation_repository

    async def execute(
        self, limit: int, cursor: str | None = None
    ) -> Tuple[List[Allocation], str | None]:
        if limit <= 0:
            return [], None

        if cursor == "":
            raise ValidationError("Cursor cannot be an empty string.")

        allocations = await self.allocation_repository.list_allocations(limit, cursor)
        next_cursor = compute_next_cursor(allocations)
        return allocations, next_cursor
