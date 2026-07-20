from typing import Tuple

from src.core.entities.allocation import Allocation
from src.core.entities.allocation_filter import AllocationFilter
from src.core.interfaces.async_allocation_repository import AsyncAllocationRepository


class UpsertAllocation:
    def __init__(self, allocation_repository: AsyncAllocationRepository):
        self.allocation_repository = allocation_repository

    async def execute(self, allocation: Allocation) -> Tuple[Allocation, bool]:
        existing_allocations = await self.allocation_repository.list_allocations_by_filter(
            limit=10000, filter={AllocationFilter.NCA_NUMBER: allocation.nca_number}
        )
        for existing in existing_allocations:
            if existing.agency == allocation.agency and existing.operating_unit == allocation.operating_unit:
                return (await self.allocation_repository.update_allocation(existing.id, allocation), False)
        return (await self.allocation_repository.create_allocation(allocation), True)
