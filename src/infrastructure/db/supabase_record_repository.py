from typing import Dict, List

from src.core.domain.record_filter import RecordFilter
from src.core.domain.record import Record
from src.core.interfaces.record_repository import RecordRepository
from src.infrastructure.db.supabase_client import client


class SupabaseRecordRepository(RecordRepository):
    def __init__(self):
        self.client = client

    def get_record_by_id(self, id: str) -> Record:
        response = self.client.table("records").select("*").eq("id", id).execute()
        data = response.model_dump().get("data", None)
        if not data:
            raise ValueError(f"Record with ID {id} not found.")
        record = Record(**data[0])
        return record

    def get_record_by_nca_number(self, nca_number: str) -> Record:
        response = (
            self.client.table("records")
            .select("*")
            .eq("nca_number", nca_number)
            .execute()
        )
        data = response.model_dump().get("data", None)
        if not data:
            raise ValueError(f"Record with NCA number {nca_number} not found.")

        record = Record(**data[0])
        return record

    def list_records(self, limit: int, cursor: str | None = None) -> List[Record]:
        query = self.client.table("records").select("*")
        if cursor is not None:
            query = query.gt("id", cursor)
        query = query.order("id", desc=False).limit(limit)

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

        query = self.client.table("records").select("*").eq(key.value, value)
        if cursor is not None:
            query = query.gt("id", cursor)
        query = query.order("id", desc=False).limit(limit)

        response = query.execute()
        data = response.model_dump().get("data", None)
        if not data:
            return []

        records = [Record(**item) for item in data]
        return records
