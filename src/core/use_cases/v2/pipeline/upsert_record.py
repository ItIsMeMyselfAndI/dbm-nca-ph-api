from typing import Tuple

from src.core.entities.record import Record
from src.core.entities.record_filter import RecordFilter
from src.core.interfaces.async_record_repository import AsyncRecordRepository


class UpsertRecord:
    def __init__(self, record_repository: AsyncRecordRepository):
        self.record_repository = record_repository

    async def execute(self, record: Record) -> Tuple[Record, bool]:
        existing_records = await self.record_repository.list_records_by_filter(
            limit=1, filter={RecordFilter.NCA_NUMBER: record.nca_number}
        )
        if existing_records:
            existing = existing_records[0]
            return (await self.record_repository.update_record(existing.id, record), False)
        return (await self.record_repository.create_record(record), True)
