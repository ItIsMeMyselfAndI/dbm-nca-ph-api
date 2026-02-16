from typing import Dict, List

from src.core.entities.allocation_filter import AllocationFilter
from src.core.entities.allocation import Allocation
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
        query = self.client.table("allocation").select("*, record!inner(released_date)")

        if cursor:
            try:
                self.get_allocation_by_id(cursor)
            except ValueError:
                raise ValueError(f"Cursor with ID {cursor} not found.")

            response = (
                self.client.table("allocation")
                .select("id, record!inner(released_date)")
                .eq("id", cursor)
                .execute()
            )
            cursor_data = response.model_dump().get("data", None)
            if (
                cursor_data
                and len(cursor_data) > 0
                and cursor_data[0].get("record", None)
            ):
                cursor_released_date = cursor_data[0].get("released_date", None)
                if cursor_released_date:
                    query = query.or_(
                        f"record.released_date.gt.{cursor_released_date},"
                        f"and(record.released_date.eq.{cursor_released_date},"
                        f"id.gt.{cursor})"
                    )
                else:
                    query = query.gt("id", cursor)

        query = (
            query.order("released_date", foreign_table="record", desc=False)
            .order("id", desc=False)
            .limit(limit)
        )

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

        query = (
            self.client.table("allocation")
            .select("*, record!inner(released_date)")
            .eq(key.value, value)
        )

        if cursor:
            try:
                self.get_allocation_by_id(cursor)
            except ValueError:
                raise ValueError(f"Cursor with ID {cursor} not found.")

            response = (
                self.client.table("allocation")
                .select("id, record!inner(released_date)")
                .eq("id", cursor)
                .execute()
            )
            cursor_data = response.model_dump().get("data", None)
            if (
                cursor_data
                and len(cursor_data) > 0
                and cursor_data[0].get("record", None)
            ):
                cursor_released_date = cursor_data[0].get("released_date", None)
                if cursor_released_date:
                    query = query.or_(
                        f"record.released_date.gt.{cursor_released_date},"
                        f"and(record.released_date.eq.{cursor_released_date},"
                        f"id.gt.{cursor})"
                    )
                else:
                    query = query.gt("id", cursor)

        query = (
            query.order("released_date", foreign_table="record", desc=False)
            .order("id", desc=False)
            .limit(limit)
        )

        response = query.execute()
        data = response.model_dump().get("data", None)
        if not data:
            return []

        allocations = [Allocation(**item) for item in data]
        return allocations
