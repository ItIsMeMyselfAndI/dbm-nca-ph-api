from src.core.exceptions import NotFoundError
from src.core.interfaces.async_allocation_repository import AsyncAllocationRepository


class DeleteAllocation:
    def __init__(self, allocation_repository: AsyncAllocationRepository):
        self.allocation_repository = allocation_repository

    async def execute(self, id: str) -> None:
        deleted = await self.allocation_repository.delete_allocation(id)
        if not deleted:
            raise NotFoundError("Allocation", id)
