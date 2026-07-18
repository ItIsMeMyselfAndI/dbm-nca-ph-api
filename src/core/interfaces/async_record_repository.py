from typing import Dict, List, Protocol

from src.core.entities.record import Record
from src.core.entities.record_filter import RecordFilter


class AsyncRecordRepository(Protocol):
    async def get_record_by_id(self, id: str) -> Record | None: ...

    async def list_records(
        self, limit: int, cursor: str | None = None
    ) -> List[Record]: ...

    async def list_records_by_filter(
        self, limit: int, filter: Dict[RecordFilter, str], cursor: str | None = None
    ) -> List[Record]: ...
