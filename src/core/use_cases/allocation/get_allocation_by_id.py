from src.core.entities.allocation import Allocation
from src.core.interfaces.allocation_repository import AllocationRepository


class GetAllocationByID:
    def __init__(self, allocation_repository: AllocationRepository):
        self.allocation_repository = allocation_repository

    def execute(self, id: str) -> Allocation:
        try:
            allocation = self.allocation_repository.get_allocation_by_id(id)
            if allocation is None:
                raise ValueError(f"Allocation with ID {id} not found.")
            return allocation

        except ValueError as e:
            raise ValueError(f"Allocation with ID {id} not found.") from e
