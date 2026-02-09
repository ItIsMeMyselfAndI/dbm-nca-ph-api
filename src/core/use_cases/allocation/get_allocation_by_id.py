from src.core.domain.allocation import Allocation
from src.core.interfaces.allocation_repository import AllocationRepository


class GetAllocationByID:
    def __init__(self, allocation_repository: AllocationRepository):
        self.allocation_repository = allocation_repository

    def execute(self, id: str) -> Allocation:
        return self.allocation_repository.get_allocation_by_id(id)
