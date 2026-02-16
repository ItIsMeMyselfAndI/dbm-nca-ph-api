from typing import List, Tuple
from src.core.entities.record import Record
from src.core.interfaces.record_repository import RecordRepository


class ListRecords:
    def __init__(self, record_repository: RecordRepository):
        self.record_repository = record_repository

    def execute(
        self, limit: int, cursor: str | None = None
    ) -> Tuple[List[Record], str | None]:
        if limit <= 0:
            return [], None

        records = self.record_repository.list_records(limit, cursor)
        if len(records) < limit:
            next_cursor = None
        else:
            next_cursor = records[-1].id
        return records, next_cursor
