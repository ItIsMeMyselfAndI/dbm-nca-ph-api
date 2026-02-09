from typing import Dict, List

from src.core.domain.allocation_filter import AllocationFilter
from src.core.domain.allocation import Allocation
from src.core.interfaces.allocation_repository import AllocationRepository
from src.infrastructure.db.supabase_client import client


class SupabaseAllocationRepository(AllocationRepository):
    def __init__(self):
        self.client = client

    def get_allocation_by_id(self, id: str) -> Allocation:
        response = self.client.table("allocation").select("*").eq("id", id).execute()
        data = response.model_dump().get("data", None)
        if not data:
            raise ValueError(f"Allocation with ID {id} not found.")

        allocation = Allocation(**data[0])
        return allocation

    def list_allocations(
        self, limit: int, cursor: str | None = None
    ) -> List[Allocation]:
        query = self.client.table("allocation").select("*")
        if cursor is not None:
            query = query.gte("id", cursor)
        query = query.order("id", desc=False).limit(limit)

        response = query.execute()
        data = response.model_dump().get("data", None)
        if not data:
            return []

        allocations = [Allocation(**item) for item in data]
        return allocations

    def list_allocations_by_filter(
        self, limit: int, filter: Dict[AllocationFilter, str], cursor: str | None = None
    ) -> List[Allocation]:
        key, value = list(filter.items())[0]

        query = self.client.table("allocation").select("*").eq(key.value, value)
        if cursor is not None:
            query = query.gte("id", cursor)
        query = query.order("id", desc=False).limit(limit)

        response = query.execute()
        data = response.model_dump().get("data", None)
        if not data:
            return []

        allocations = [Allocation(**item) for item in data]
        return allocations
