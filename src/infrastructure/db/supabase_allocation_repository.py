from typing import List
from supabase import Client

from core.domain.allocation import Allocation
from core.interfaces.allocation_repository import AllocationRepository


class SupabaseAllocationRepository(AllocationRepository):
    def __init__(self, client: Client):
        self.client = client

    def get_allocation_by_id(self, allocation_id: str) -> Allocation:
        response = (
            self.client.table("allocations")
            .select("*")
            .eq("id", allocation_id)
            .execute()
        )
        data = response.data
        if not data:
            raise ValueError(f"Allocation with ID {allocation_id} not found.")
        allocation = Allocation(**data[0])
        return allocation

    def list_allocations(self, cursor: int, limit: int) -> List[Allocation]:
        response = (
            self.client.table("allocations")
            .select("*")
            .range(cursor, cursor + limit - 1)
            .execute()
        )
        data = response.data
        if not data:
            return []
        allocations = [Allocation(**item) for item in data]
        return allocations

    def list_allocations_by_agency(
        self, agency_id: str, cursor: int, limit: int
    ) -> List[Allocation]:
        response = (
            self.client.table("allocations")
            .select("*")
            .eq("agency_id", agency_id)
            .range(cursor, cursor + limit - 1)
            .execute()
        )
        data = response.data
        if not data:
            return []
        allocations = [Allocation(**item) for item in data]
        return allocations

    def list_allocations_by_nca_number(
        self, nca_number: str, cursor: int, limit: int
    ) -> List[Allocation]:
        response = (
            self.client.table("allocations")
            .select("*")
            .eq("nca_number", nca_number)
            .range(cursor, cursor + limit - 1)
            .execute()
        )
        data = response.data
        if not data:
            return []
        allocations = [Allocation(**item) for item in data]
        return allocations

    def list_allocations_by_operating_unit(
        self, operating_unit: str, cursor: int, limit: int
    ) -> List[Allocation]:
        response = (
            self.client.table("allocations")
            .select("*")
            .eq("operating_unit", operating_unit)
            .range(cursor, cursor + limit - 1)
            .execute()
        )
        data = response.data
        if not data:
            return []
        allocations = [Allocation(**item) for item in data]
        return allocations
