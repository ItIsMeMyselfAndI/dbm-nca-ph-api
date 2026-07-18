from src.core.entities.allocation import Allocation
from src.core.exceptions import NotFoundError
from src.core.interfaces.async_allocation_repository import AsyncAllocationRepository


class GetAllocationByID:
    def __init__(self, allocation_repository: AsyncAllocationRepository):
        self.allocation_repository = allocation_repository

    async def execute(self, id: str) -> Allocation:
        allocation = await self.allocation_repository.get_allocation_by_id(id)
        if allocation is None:
            raise NotFoundError("Allocation", id)
        return allocation
