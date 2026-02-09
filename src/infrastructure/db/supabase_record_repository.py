from typing import List

from core.domain.record import Record
from core.interfaces.record_repository import RecordRepository


class SupabaseRecordRepository(RecordRepository):
    def __init__(self, client):
        self.client = client

    def get_record_by_id(self, record_id: str) -> Record:
        response = (
            self.client.table("records").select("*").eq("id", record_id).execute()
        )
        data = response.data
        if not data:
            raise ValueError(f"Record with ID {record_id} not found.")
        record = Record(**data[0])
        return record

    def get_record_by_nca_number(self, nca_number: str) -> Record:
        response = (
            self.client.table("records")
            .select("*")
            .eq("nca_number", nca_number)
            .execute()
        )
        data = response.data
        if not data:
            raise ValueError(f"Record with NCA number {nca_number} not found.")
        record = Record(**data[0])
        return record

    def list_records(self, cursor: int, limit: int) -> List[Record]:
        response = (
            self.client.table("records")
            .select("*")
            .range(cursor, cursor + limit - 1)
            .execute()
        )
        data = response.data
        if not data:
            return []
        records = [Record(**item) for item in data]
        return records

    def list_records_by_department(
        self, department_id: str, cursor: int, limit: int
    ) -> List[Record]:
        response = (
            self.client.table("records")
            .select("*")
            .eq("department_id", department_id)
            .range(cursor, cursor + limit - 1)
            .execute()
        )
        data = response.data
        if not data:
            return []
        records = [Record(**item) for item in data]
        return records

    def list_records_by_nca_type(
        self, nca_type: str, cursor: int, limit: int
    ) -> List[Record]:
        response = (
            self.client.table("records")
            .select("*")
            .eq("nca_type", nca_type)
            .range(cursor, cursor + limit - 1)
            .execute()
        )
        data = response.data
        if not data:
            return []
        records = [Record(**item) for item in data]
        return records

    def list_records_by_release_id(
        self, release_id: str, cursor: int, limit: int
    ) -> List[Record]:
        response = (
            self.client.table("records")
            .select("*")
            .eq("release_id", release_id)
            .range(cursor, cursor + limit - 1)
            .execute()
        )
        data = response.data
        if not data:
            return []
        records = [Record(**item) for item in data]
        return records

    def list_records_by_released_date(
        self, released_date: str, cursor: int, limit: int
    ) -> List[Record]:
        response = (
            self.client.table("records")
            .select("*")
            .eq("released_date", released_date)
            .range(cursor, cursor + limit - 1)
            .execute()
        )
        data = response.data
        if not data:
            return []
        records = [Record(**item) for item in data]
        return records
