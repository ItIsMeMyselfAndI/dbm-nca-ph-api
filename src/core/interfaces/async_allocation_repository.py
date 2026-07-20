from typing import Dict, List, Protocol

from src.core.entities.allocation import Allocation
from src.core.entities.allocation_filter import AllocationFilter


class AsyncAllocationRepository(Protocol):
    async def get_allocation_by_id(self, id: str) -> Allocation | None: ...

    async def list_allocations(
        self, limit: int, cursor: str | None = None
    ) -> List[Allocation]: ...

    async def list_allocations_by_filter(
        self,
        limit: int,
        filter: Dict[AllocationFilter, str],
        cursor: str | None = None,
    ) -> List[Allocation]: ...

    async def create_allocation(self, allocation: Allocation) -> Allocation: ...

    async def update_allocation(
        self, id: str, allocation: Allocation
    ) -> Allocation | None: ...

    async def delete_allocation(self, id: str) -> bool: ...
