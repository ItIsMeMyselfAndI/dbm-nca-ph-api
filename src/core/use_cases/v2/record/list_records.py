from typing import List, Tuple

from src.core.entities.record import Record
from src.core.exceptions import ValidationError
from src.core.interfaces.async_record_repository import AsyncRecordRepository
from src.core.use_cases.v2._cursor import compute_next_cursor


class ListRecords:
    def __init__(self, record_repository: AsyncRecordRepository):
        self.record_repository = record_repository

    async def execute(
        self, limit: int, cursor: str | None = None
    ) -> Tuple[List[Record], str | None]:
        if limit <= 0:
            return [], None

        if cursor == "":
            raise ValidationError("Cursor cannot be an empty string.")

        records = await self.record_repository.list_records(limit, cursor)
        next_cursor = compute_next_cursor(records)
        return records, next_cursor
