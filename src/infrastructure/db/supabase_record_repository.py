from typing import Dict, List

from src.core.entities.record_filter import RecordFilter
from src.core.entities.record import Record
from src.core.interfaces.record_repository import RecordRepository
from src.infrastructure.db.supabase_client import client


class SupabaseRecordRepository(RecordRepository):
    def __init__(self):
        self.client = client

    def get_record_by_id(self, id: str) -> Record | None:
        response = self.client.table("record").select("*").eq("id", id).execute()
        data = response.model_dump().get("data", None)
        if not data:
            return None
        record = Record(**data[0])
        return record

    def list_records(self, limit: int, cursor: str | None = None) -> List[Record]:
        query = self.client.table("record").select("*")

        if cursor:
            response = (
                self.client.table("record")
                .select("released_date")
                .eq("id", cursor)
                .execute()
            )
            cursor_data = response.model_dump().get("data", None)
            if cursor_data and len(cursor_data) > 0:
                cursor_released_date = cursor_data[0].get("released_date", None)
                if cursor_released_date:
                    query = query.or_(
                        f"released_date.gt.{cursor_released_date},"
                        f"and(released_date.eq.{cursor_released_date},"
                        f"id.gt.{cursor})"
                    )
                else:
                    query = query.gt("id", cursor)

        query = (
            query.order("released_date", desc=False)
            .order("id", desc=False)
            .limit(limit)
        )

        response = query.execute()
        data = response.model_dump().get("data", None)
        if not data:
            return []

        records = [Record(**item) for item in data]
        return records

    def list_records_by_filter(
        self, limit: int, filter: Dict[RecordFilter, str], cursor: str | None = None
    ) -> List[Record]:
        key, value = list(filter.items())[0]

        query = self.client.table("record").select("*").eq(key.value, value)

        if cursor:
            response = (
                self.client.table("record")
                .select("released_date")
                .eq("id", cursor)
                .execute()
            )
            cursor_data = response.model_dump().get("data", None)
            if cursor_data and len(cursor_data) > 0:
                cursor_released_date = cursor_data[0].get("released_date", None)
                if cursor_released_date:
                    query = query.or_(
                        f"released_date.gt.{cursor_released_date},"
                        f"and(released_date.eq.{cursor_released_date},"
                        f"id.gt.{cursor})"
                    )
                else:
                    query = query.gt("id", cursor)

        query = (
            query.order("released_date", desc=False)
            .order("id", desc=False)
            .limit(limit)
        )

        response = query.execute()
        data = response.model_dump().get("data", None)
        if not data:
            return []

        records = [Record(**item) for item in data]
        return records
