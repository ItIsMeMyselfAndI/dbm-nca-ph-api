from typing import Dict, List, Tuple

from src.core.domain.allocation import Allocation
from src.core.domain.allocation_filter import AllocationFilter
from src.core.interfaces.allocation_repository import AllocationRepository


class ListAllocationsByFilter:
    def __init__(self, allocation_repository: AllocationRepository):
        self.allocation_repository = allocation_repository

    def execute(
        self, limit: int, filter: Dict[AllocationFilter, str], cursor: str | None = None
    ) -> Tuple[List[Allocation], str | None]:
        allocations = self.allocation_repository.list_allocations_by_filter(
            limit + 1, filter, cursor
        )
        has_more = len(allocations) == limit + 1

        next_cursor = allocations[-1].id if has_more else None
        relevant_allocations = allocations[: limit + 1]
        return relevant_allocations, next_cursor
