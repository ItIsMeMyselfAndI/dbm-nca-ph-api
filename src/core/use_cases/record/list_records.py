from typing import List, Tuple
from src.core.entities.record import Record
from src.core.interfaces.record_repository import RecordRepository


class ListRecords:
    def __init__(self, record_repository: RecordRepository):
        self.record_repository = record_repository

    def execute(
        self, limit: int, cursor: str | None = None
    ) -> Tuple[List[Record], str | None]:
        records = self.record_repository.list_records(limit + 1, cursor)
        has_more = len(records) == limit + 1

        next_cursor = records[-1].id if has_more else None
        relevant_records = records[:limit]
        return relevant_records, next_cursor
