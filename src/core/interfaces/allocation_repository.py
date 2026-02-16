from typing import Dict, List, Protocol

from src.core.entities.allocation_filter import AllocationFilter
from src.core.entities.allocation import Allocation


class AllocationRepository(Protocol):
    def get_allocation_by_id(self, id: str) -> Allocation | None:
        """Get an allocation by its ID."""
        ...

    def list_allocations(
        self, limit: int, cursor: str | None = None
    ) -> List[Allocation]:
        """List all allocations with pagination."""
        ...

    def list_allocations_by_filter(
        self,
        limit: int,
        filter: Dict[AllocationFilter, str],
        cursor: str | None = None,
    ) -> List[Allocation]:
        """List filtered allocations with pagination."""
        ...
