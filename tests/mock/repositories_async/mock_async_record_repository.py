import json
from pathlib import Path
from typing import Dict, List

from src.core.entities.record import Record
from src.core.entities.record_filter import RecordFilter


class MockAsyncRecordRepository:
    def __init__(self):
        self.records = self._get_mock_records()

    def _get_mock_records(self):
        base_path = Path(__file__).parent.parent
        json_path = base_path / "data" / "records.json"
        with open(json_path) as f:
            data = json.load(f)
        return [Record(**item) for item in data]

    async def get_record_by_id(self, id: str) -> Record | None:
        id = id.strip().lower()
        return next((r for r in self.records if r.id == id), None)

    async def list_records(self, limit: int, cursor: str | None = None) -> List[Record]:
        records = self.records
        if cursor:
            cursor = cursor.strip().lower()
            idx = next((i for i, r in enumerate(self.records) if r.id == cursor), None)
            if idx is None:
                return []
            records = self.records[idx + 1 :]
        return records[:limit]

    async def list_records_by_filter(
        self, limit: int, filter: Dict[RecordFilter, str], cursor: str | None = None
    ) -> List[Record]:
        records = self.records
        if cursor:
            cursor = cursor.strip().lower()
            idx = next((i for i, r in enumerate(self.records) if r.id == cursor), None)
            if idx is None:
                return []
            records = self.records[idx + 1 :]
        key, value = list(filter.items())[0]
        records = [r for r in records if getattr(r, key.value) == value]
        return records[:limit]
