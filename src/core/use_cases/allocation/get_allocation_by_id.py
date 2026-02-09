from core.interfaces.allocation_repository import AllocationRepository


class GetAllocationById:
    def __init__(self, allocation_repository: AllocationRepository):
        self.allocation_repository = allocation_repository

    def execute(self, allocation_id: str):
        return self.allocation_repository.get_allocation_by_id(allocation_id)
