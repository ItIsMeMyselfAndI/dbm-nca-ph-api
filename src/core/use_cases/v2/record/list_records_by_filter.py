from typing import Dict, List, Tuple

from src.core.entities.record import Record
from src.core.entities.record_filter import RecordFilter
from src.core.exceptions import ValidationError
from src.core.interfaces.async_record_repository import AsyncRecordRepository
from src.core.use_cases.v2._cursor import compute_next_cursor


class ListRecordsByFilter:
    def __init__(self, record_repository: AsyncRecordRepository):
        self.record_repository = record_repository

    async def execute(
        self, limit: int, filter: Dict[RecordFilter, str], cursor: str | None = None
    ) -> Tuple[List[Record], str | None]:
        if limit <= 0:
            return [], None

        if cursor == "":
            raise ValidationError("Cursor cannot be an empty string.")

        records = await self.record_repository.list_records_by_filter(
            limit, filter, cursor
        )
        next_cursor = compute_next_cursor(records)
        return records, next_cursor
