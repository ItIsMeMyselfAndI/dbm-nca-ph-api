from typing import Dict, List, Tuple

from src.core.domain.record import Record
from src.core.domain.record_filter import RecordFilter
from src.core.interfaces.record_repository import RecordRepository


class ListRecordsByFilter:
    def __init__(self, record_repository: RecordRepository):
        self.record_repository = record_repository

    def execute(
        self, limit: int, filter: Dict[RecordFilter, str], cursor: str | None = None
    ) -> Tuple[List[Record], str | None]:
        records = self.record_repository.list_records_by_filter(
            limit + 1, filter, cursor
        )
        has_more = len(records) == limit + 1

        next_cursor = records[-1].id if has_more else None
        relevant_records = records[: limit + 1]
        return relevant_records, next_cursor
