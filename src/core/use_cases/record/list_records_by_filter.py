from typing import Dict, List, Tuple

from src.core.entities.record import Record
from src.core.entities.record_filter import RecordFilter
from src.core.interfaces.record_repository import RecordRepository


class ListRecordsByFilter:
    def __init__(self, record_repository: RecordRepository):
        self.record_repository = record_repository

    def execute(
        self, limit: int, filter: Dict[RecordFilter, str], cursor: str | None = None
    ) -> Tuple[List[Record], str | None]:
        if limit <= 0:
            return [], None

        records = self.record_repository.list_records_by_filter(limit, filter, cursor)
        if len(records) < limit:
            next_cursor = None
        else:
            next_cursor = records[-1].id
        return records, next_cursor
